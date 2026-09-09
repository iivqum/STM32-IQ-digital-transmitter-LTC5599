
This is a simple 8-bit IQ transmitter using the STM32G431 for baseband generation. An LMX2571 is used to generate a carrier from 10 MHz to around 1.35 GHz which feeds
an LT5599 quadrature modulator.

Baseband bandwidth is around 100 KHz. In principle this could be increased, however I can't get any more than around 600 KB/s writes on this particular part, even with
an optimal host.

<p align="center"><img width="586" height="520" alt="PCB" src="https://github.com/user-attachments/assets/fa2edd82-dd9e-400b-bf28-0493594522bb" /></p>
