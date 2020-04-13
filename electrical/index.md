---
layout: default
title: Electrical Setup
---
# <i class="fad fa-outlet"></i> Electrical Setup
---
### <i class="fas fa-play-circle"></i> Getting Started 
If you have little experience with wiring with electronics, then it is strongly recommended to read up on the proper precautions that need to be taken [here](https://electrical-engineering-portal.com/21-safety-rules-for-working-with-electrical-equipment). Along a similar vein, if you have never soldered, then a breadboard can be used to wire the whole project. Breadboard connections are less durable than a solder joint, but jumper cables allow you to avoid soldering.

Building an automatic liquid handler follows many of the principles used by DIYers to build 3D printers and CNC routers, which are found in many households. It is recommended to watch videos such as this [one](https://youtu.be/qub5chyIQ0s) to learn the operating principles behind stepper motors, stepper drivers, limit switches, etc. 

### <i class="fas fa-plug"></i> Electrical System Components
Roughly there are three main parts of OTTO's electrical system:
- The microcontroller
- The stepper drivers and motors
- Sensors and buttons

Check out the bill of materials for part numbers, quantities, and retailers <i class="fas fa-list-ol"></i> Bill of materials for the electrical components. 

### <i class="fas fa-microchip"></i> Microcontroller

It’s the microcontroller’s job to translate positional coordinates sent over as G-code from a computer into stepper motor movements. This job includes not only barking orders, like telling the stepper drivers when and in what direction to move the motors, but also requires the microcontroller to listen and respond to various inputs like the extruder temperature or the state of the limit switches.

A microcontroller is housed on a motherboard, which provides the components that the microcontroller requires to operated (i.e., 3.3V) and the terminals for users to connect various electrical devices to. The most popular microcontroller/motherboard combo is either the ATmega328P/Arduino Uno or the ATmega2560/Arduino Mega. Neither of these boards were used for OTTO because these 8-bit processors were unable to produce enough step pulses when running the AccelStepper library (see [software section](https://openliquidhandler.com/software) for more information). We instead used the Arduino Due which is powered by the snappy 32-bit ARM core microcontroller. 

If you are familiar with CNC controller boards, then perhaps you are wondering why we did not use an all-in-one motherboard that includes not only the microcontroller but also the stepper drivers. First off, it is possible to run OTTO with one of these boards and they definitely cut down on a lot of wiring, but these boards typically do not have stepper drivers capable of driving the power hungry Nema23 motors that are used to move the gantry.

### <i class="fad fa-cog"></i> Stepper Motors and Drivers
The first step is to wire all stepper motors to the stepper drivers. It is recommended to watch this [video](https://www.youtube.com/watch?v=IEmGOuMFPKQ) if you require more information than the schematic below.

Next, the stepper drivers need to be wired to Arduino Due and power supply. For this project, TMC2660 drivers were used. These are more complicated than the run-of-the-mill stepper drivers because they communicate with the Due through a Serial Peripheral Interface (SPI) connection, which allows the motor current and microstepping to be set digitally. This is very helpful when calibrating the system. The TMC2660 also have a lot of other features, such as near silent operation. You can find their datasheet [here](https://www.trinamic.com/products/integrated-circuits/details/tmc2660-pa/) to learn more about them. With these added features comes more wiring. The SDO, SDI, SCK, CSN pins on the driver needs to be connected to their respective pins on the Due outlined below. An in depth guide on SPI is available on the [Arduino website](https://www.arduino.cc/en/reference/SPI"). If you are overwhelmed by all the wiring you can use a more basic stepper driver like the [TB6600](https://www.amazon.com/dp/B07B9ZQF5D/ref=cm_sw_em_r_mt_dp_U_AF.KEb8BAKC99) that doesn’t use SPI. The only requirements for the stepper drivers are that they support Bipolar hybrid stepper drivers and can supply at least 2A of current.


#### X-axis
<table class="table">
  <thead>
    <tr>
      <th scope="col">Stepper Driver Pin</th>
      <th scope="col">Arduino Pin</th>
    </tr>
  </thead>
  <thead>
    <tr>
      <th scope="col">X-Axis</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">1</th>
      <td>Mark</td>
    </tr>
    <tr>
      <th scope="row">2</th>
      <td>Jacob</td>
    </tr>
    <tr>
      <th scope="row">3</th>
      <td>Larry</td>
    </tr>
  </tbody>
</table>

![Otto, the open-source automatic liquid handler](../assets/img/electrical/Stepper-Motor-wiring.jpg)
