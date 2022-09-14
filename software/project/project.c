#include "system.h"
#include "altera_up_avalon_accelerometer_spi.h"
#include "altera_avalon_timer_regs.h"
#include "altera_avalon_timer.h"
#include "altera_avalon_pio_regs.h"
#include "sys/alt_irq.h"
#include <stdlib.h>
#include <sys/alt_stdio.h>
#include <stdio.h>

#define OFFSET -32
#define PWM_PERIOD 16

alt_8 pwm = 0;
alt_u8 led;
int level;

void led_write(alt_u8 led_pattern) {
    IOWR(LED_BASE, 0, led_pattern);
}

void convert_read(alt_32 acc_read, int * level, alt_u8 * led) {
    acc_read += OFFSET;
    alt_u8 val = (acc_read >> 6) & 0x07;
    * led = (8 >> val) | (8 << (8 - val));
    * level = (acc_read >> 1) & 0x1f;
}

void sys_timer_isr() {
    IOWR_ALTERA_AVALON_TIMER_STATUS(TIMER_BASE, 0);

    if (pwm < abs(level)) {

        if (level < 0) {
            led_write(led << 1);
        } else {
            led_write(led >> 1);
        }

    } else {
        led_write(led);
    }

    if (pwm > PWM_PERIOD) {
        pwm = 0;
    } else {
        pwm++;
    }

}

void timer_init(void * isr) {

    IOWR_ALTERA_AVALON_TIMER_CONTROL(TIMER_BASE, 0x0003);
    IOWR_ALTERA_AVALON_TIMER_STATUS(TIMER_BASE, 0);
    IOWR_ALTERA_AVALON_TIMER_PERIODL(TIMER_BASE, 0x0900);
    IOWR_ALTERA_AVALON_TIMER_PERIODH(TIMER_BASE, 0x0000);
    alt_irq_register(TIMER_IRQ, 0, isr);
    IOWR_ALTERA_AVALON_TIMER_CONTROL(TIMER_BASE, 0x0007);

}

int main() {
	alt_32 switch_datain;
	alt_32 change;

    alt_32 x_read;
    alt_32 y_read;
    alt_up_accelerometer_spi_dev * acc_dev;
    acc_dev = alt_up_accelerometer_spi_open_dev("/dev/accelerometer_spi");
    if (acc_dev == NULL) { // if return 1, check if the spi ip name is "accelerometer_spi"
        return 1;
    }
    switch_datain = ~IORD_ALTERA_AVALON_PIO_DATA(SWITCH_BASE);

    timer_init(sys_timer_isr);
    while (1) {
    	change = x_read/10;
        alt_up_accelerometer_spi_read_x_axis(acc_dev, & x_read);
        if(change!=x_read/10){
        	alt_printf("raw x data: %x\n", x_read/10);
        }
    	change = y_read/10;
        alt_up_accelerometer_spi_read_y_axis(acc_dev, & y_read);
        if(change!=y_read/10){
        	alt_printf("raw y data: %x\n", y_read/10);
        }
        convert_read(x_read, & level, & led);
        change = switch_datain;
        switch_datain = ~IORD_ALTERA_AVALON_PIO_DATA(SWITCH_BASE);
        //Mask the bits so the leftmost LEDs are off (we only care about LED3-0)
        switch_datain &= (0b0000000001);
        if(change!=switch_datain){
        	alt_printf("switch data: %x\n", switch_datain);
        }//else{
        //	alt_printf("No_Change");
        //}
        //Send the data to the LED
        //IOWR_ALTERA_AVALON_PIO_DATA(LED_BASE,button_datain);

    }


    return 0;
}

