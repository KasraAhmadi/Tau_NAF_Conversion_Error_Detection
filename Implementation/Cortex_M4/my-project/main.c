#include <libopencm3/stm32/rcc.h>
#include <libopencm3/stm32/gpio.h>
#include <libopencm3/cm3/nvic.h>
#include <libopencm3/cm3/systick.h>
#include <libopencm3/stm32/usart.h>
#include "helper.h"
static volatile unsigned long long overflowcnt = 0;
uint64_t hal_get_time()
{
	while (true)
	{
		unsigned long long before = overflowcnt;
		unsigned long long result = (before + 1) * 16777216llu - systick_get_value();
		if (overflowcnt == before)
		{
			return result;
		}
	}
}
static void systick_setup(void)
{

	systick_set_clocksource(STK_CSR_CLKSOURCE_AHB);
	systick_set_reload(0xFFFFFFu);
	systick_interrupt_enable();
	systick_counter_enable();
}
void sys_tick_handler(void)
{
	++overflowcnt;
}
static void clock_setup(void)
{
	/* Enable GPIOD clock for LED & USARTs. */
	rcc_periph_clock_enable(RCC_GPIOD);
	rcc_periph_clock_enable(RCC_GPIOA);

	/* Enable clocks for USART2. */
	rcc_periph_clock_enable(RCC_USART2);
}
static void usart_setup(void)
{
	/* Setup USART2 parameters. */
	usart_set_baudrate(USART2, 115200);
	usart_set_databits(USART2, 8);
	usart_set_stopbits(USART2, USART_STOPBITS_1);
	usart_set_mode(USART2, USART_MODE_TX);
	usart_set_parity(USART2, USART_PARITY_NONE);
	usart_set_flow_control(USART2, USART_FLOWCONTROL_NONE);

	/* Finally enable the USART. */
	usart_enable(USART2);
}
static void gpio_setup(void)
{
	/* Setup GPIO pin GPIO12 on GPIO port D for LED. */
	gpio_mode_setup(GPIOD, GPIO_MODE_OUTPUT, GPIO_PUPD_NONE, GPIO12);

	/* Setup GPIO pins for USART2 transmit. */
	gpio_mode_setup(GPIOA, GPIO_MODE_AF, GPIO_PUPD_NONE, GPIO2);

	/* Setup USART2 TX pin as alternate function. */
	gpio_set_af(GPIOA, GPIO_AF7, GPIO2);
}
void send_unsignedll(const char *s, unsigned long long c)
{
	int i = 0;
	char outs[21] = {0};
	if (c < 10)
	{
		outs[0] = '0' + c;
	}
	else
	{
		i = 19;
		while (c != 0)
		{
			/* Method adapted from ""hackers delight":
			   Creates an approximation of q = (8/10) */
			unsigned long long q = (c >> 1) + (c >> 2);
			q = q + (q >> 4);
			q = q + (q >> 8);
			q = q + (q >> 16);
			q = q + (q >> 32);
			/* Now q = (1/10) */
			q = q >> 3;
			/* Since q contains an error due to the bits shifted out of the value, we
			   only use it to determine the remainder.  */
			unsigned long long r = c - ((q << 3) + (q << 1));
			c = q;
			/* The remainder might be off by 10, so q may be off by 1 */
			if (r > 9)
			{
				c += 1;
				r -= 10;
			}
			outs[i] = '0' + (unsigned)r;
			i -= 1;
		}
		i += 1;
	}
	hal_send_str(s);
	hal_send_str(outs + i);
	hal_send_str("\r\n");
}
void hal_send_str(const char *in)
{
	const char *cur = in;
	while (*cur)
	{
		usart_send_blocking(USART2, *cur);
		cur += 1;
	}
	// usart_send_blocking(USART2, '\r\n');
}

int main(void)
{
	unsigned long long t0, t1,t2,t3;
	int i;

	clock_setup();
	gpio_setup();
	usart_setup();
	systick_setup();
	unsigned long long old = overflowcnt;
	while (old == overflowcnt);
	hal_send_str("=============Tau Conversion begin=============\r\n");
	while (1)
	{
		t0 = hal_get_time();
		Generate_NAF();
		t1 = hal_get_time();
		send_unsignedll("Generate_NAF cycles:", t1 - t0);
		t0 = hal_get_time();
		Generate_NAF_CC();
		t1 = hal_get_time();
		send_unsignedll("Generate_NAF_CC cycles:", t1-t0);
		t0 = hal_get_time();
		Generate_double_NAF();
		t1 = hal_get_time();
		send_unsignedll("Generate_double_NAF cycles:", t1-t0);
		t0 = hal_get_time();
		Generate_double_NAF_CC();
		t1 = hal_get_time();
		send_unsignedll("Generate_double_NAF_CC cycles:", t1-t0);
		t0 = hal_get_time();
		Generate_best_double_NAF_CC();
		t1 = hal_get_time();
		send_unsignedll("Generate_best_double_NAF_CC cycles:", t1-t0);
	}

	return 0;
}