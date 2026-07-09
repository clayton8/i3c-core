## **I3C[®] Application Note: General Topics** 

## **Applies to MIPI I3C v1.1+ and MIPI I3C Basic v1.1.1+** 

**App Note Version 1.1 27 April 2022** 

MIPI Board Approved 27 July 2022 **Public Release Edition** 

This is an informative document, not a MIPI Specification. MIPI member companies’ rights and obligations apply to this Supporting Document as defined in the MIPI Membership Agreement and MIPI Bylaws. 

Various rights and obligations that apply solely to MIPI Specifications (as defined in the MIPI Membership Agreement and MIPI Bylaws) including, but not limited to, patent license rights and obligations, do not apply to this document. 

This document is subject to further editorial and technical development. 

Copyright © 2018–2022 MIPI Alliance, Inc. 

App Note for I3C: General Topics 

App Note Version 1.1 27-Apr-2022 

## **NOTICE OF DISCLAIMER** 

The material contained herein is provided on an “AS IS” basis. To the maximum extent permitted by applicable law, this material is provided AS IS AND WITH ALL FAULTS, and the authors and developers of this material and MIPI Alliance Inc. (“MIPI”) hereby disclaim all other warranties and conditions, either express, implied or statutory, including, but not limited to, any (if any) implied warranties, duties or conditions of merchantability, of fitness for a particular purpose, of accuracy or completeness of responses, of results, of workmanlike effort, of lack of viruses, and of lack of negligence. ALSO, THERE IS NO WARRANTY OR CONDITION OF TITLE, QUIET ENJOYMENT, QUIET POSSESSION, CORRESPONDENCE TO DESCRIPTION OR NON-INFRINGEMENT WITH REGARD TO THIS MATERIAL. 

IN NO EVENT WILL ANY AUTHOR OR DEVELOPER OF THIS MATERIAL OR MIPI BE LIABLE TO ANY OTHER PARTY FOR THE COST OF PROCURING SUBSTITUTE GOODS OR SERVICES, LOST PROFITS, LOSS OF USE, LOSS OF DATA, OR ANY INCIDENTAL, CONSEQUENTIAL, DIRECT, INDIRECT, OR SPECIAL DAMAGES WHETHER UNDER CONTRACT, TORT, WARRANTY, OR OTHERWISE, ARISING IN ANY WAY OUT OF THIS OR ANY OTHER AGREEMENT RELATING TO THIS MATERIAL, WHETHER OR NOT SUCH PARTY HAD ADVANCE NOTICE OF THE POSSIBILITY OF SUCH DAMAGES. 

The material contained herein is not a license, either expressly or impliedly, to any IPR owned or controlled by any of the authors or developers of this material or MIPI. Any license to use this material is granted separately from this document. This material is protected by copyright laws, and may not be reproduced, republished, distributed, transmitted, displayed, broadcast or otherwise exploited in any manner without the express prior written permission of MIPI Alliance. MIPI, MIPI Alliance and the dotted rainbow arch and all related trademarks, service marks, tradenames, and other intellectual property are the exclusive property of MIPI Alliance Inc. and cannot be used without its express prior written permission. The use or implementation of this material may involve or require the use of intellectual property rights (“IPR”) including (but not limited to) patents, patent applications, or copyrights owned by one or more parties, whether or not members of MIPI. MIPI does not make any search or investigation for IPR, nor does MIPI require or request the disclosure of any IPR or claims of IPR as respects the contents of this material or otherwise. 

Without limiting the generality of the disclaimers stated above, users of this material are further notified that MIPI: (a) does not evaluate, test or verify the accuracy, soundness or credibility of the contents of this material; (b) does not monitor or enforce compliance with the contents of this material; and (c) does not certify, test, or in any manner investigate products or services or any claims of compliance with MIPI specifications or related material. 

Questions pertaining to this material, or the terms or conditions of its provision, should be addressed to: 

MIPI Alliance, Inc. c/o IEEE-ISTO 445 Hoes Lane, Piscataway New Jersey 08854, United States Attn: Managing Director 

## **Special Note Concerning I3C and I3C Basic** 

As described in the I3C Basic specification, certain parties have agreed to grant additional rights to I3C Basic implementers, beyond those rights granted under the MIPI Membership Agreement or MIPI Bylaws. Contribution to or other participation in the development of this App Note document does not create any implication that a party has agreed to grant any additional rights in connection with I3C Basic. Consistent with the statements above, nothing in or about this App Note document alters any party’s rights or obligations associated with I3C or I3C Basic. 

ii 

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

App Note Version 1.1 27-Apr-2022 

App Note for I3C: General Topics 

## **Contents** 

|**Contents**|**Contents**|**Contents**|
|---|---|---|
|**Figures .................................................................................................................................v**|||
|**Release History ................................................................................................................. vi**|||
|**1**|**Introduction .................................................................................................................1**||
||1.1|Scope ............................................................................................................................... 1|
|**2**|**Terminology .................................................................................................................2**||
||2.1|Definitions ....................................................................................................................... 2|
||2.2|Abbreviations ................................................................................................................... 2|
||2.3|Acronyms ......................................................................................................................... 2|
|**3**|**References ....................................................................................................................3**||
|**4**|**Overview ......................................................................................................................5**||
||4.1|Supported Topologies ...................................................................................................... 5|
||4.2|Using Added Functionality .............................................................................................. 5|
|**5**|**System Integration Guidelines ...................................................................................7**||
||5.1|I3C Bus Operation ........................................................................................................... 7|
||5.1.1|Format of Data Transfer Units ...................................................................................... 8|
||5.1.2|Bus Transfers ................................................................................................................ 9|
||5.1.3|SDA Line Discipline ................................................................................................... 11|
||5.1.4|High Data Rates (HDR Modes) .................................................................................. 11|
||5.2|I3C Device Characteristics ............................................................................................ 12|
||5.2.1|Devices Roles and Responsibilities ............................................................................ 13|
||5.2.2|Clock-to-Data Turnaround Time (tSCO) ....................................................................... 16|
||5.2.3|Pad Capacitance .......................................................................................................... 16|
||5.2.4|Pad Drive Strength ..................................................................................................... 16|
||5.2.5|BCR Use ..................................................................................................................... 17|
||5.3|Dynamic Address Assignment (DAA) ........................................................................... 19|
||5.3.1|Dynamic Address Assignment Procedure ................................................................... 19|
||5.3.2|Dynamic Address Consistency ................................................................................... 21|
||5.3.3|Address Assignment Guidance ................................................................................... 21|
||5.4|Use of Legacy I2C Devices ............................................................................................ 24|
||5.4.1|Considerations for Legacy I2C Devices ...................................................................... 24|
||5.4.2|I2C Clock Stretch is Not Allowed in I3C .................................................................... 26|
||5.4.3|Legacy Virtual Register (LVR) Use ............................................................................ 26|
||5.5|I/O Characteristics ......................................................................................................... 27|
||5.5.1|Pad Capacitance .......................................................................................................... 27|
||5.5.2|SDA Drive Strength .................................................................................................... 27|
||5.6|Bus Topologies .............................................................................................................. 28|
||5.6.1|Bus Topology Types ................................................................................................... 28|
||5.6.2|Trace/Medium ............................................................................................................ 31|
||5.6.3|Mixed Bus Considerations ......................................................................................... 32|
||5.6.4|Hot-Join Capability .................................................................................................... 32|



Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

App Note for I3C: General Topics 

App Note Version 1.1 27-Apr-2022 

|5.7|Physical/Electrical/Testing Considerations (I3C CTS) .................................................. 33|
|---|---|
|5.8|Bus High-Keeper ........................................................................................................... 34|
|5.9|Bridge Devices............................................................................................................... 35|



iv 

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

App Note Version 1.1 27-Apr-2022 

App Note for I3C: General Topics 

## **Figures** 

Figure 1 I3C Transfer Types ........................................................................................................... 10 Figure 2 Components of Clock-to-Data Turnaround Delay (tSCO) ................................................. 16 Figure 3 Bus Characteristics Register (BCR) ................................................................................. 17 Figure 4 Dynamic Address Assignment Transaction ...................................................................... 20 Figure 5 Spike Filter Detection Pattern .......................................................................................... 25 Figure 6 Multi-Drop Bus Topology ................................................................................................ 28 Figure 7 Point-to-Point Bus Topology ............................................................................................ 29 Figure 8 Star-on-Stick Bus Topology ............................................................................................. 29 Figure 9 Complex Bus Topology .................................................................................................... 30 

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

App Note for I3C: General Topics 

App Note Version 1.1 27-Apr-2022 

## **Release History** 

||||
|---|---|---|
|**Date**|**Version**|**Description**|
|08-Dec-2018|v1.0|Initial Board approved release.|
|27-Jul-2022|v1.1|Board approved release.|



vi 

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

App Note Version 1.1 27-Apr-2022 

App Note for I3C: General Topics 

## `1` **1 Introduction** 

- `2` The MIPI I3C Bus interface _**[MIPI06]**_ is an evolutionary specification that improves upon the legacy I²C `3` standard. It is designed to reduce the number of physical pins used in sensor system integration, and `4` supports low-power, high-speed digital communication typically associated with UART and SPI interfaces. 

- `5` 

## _**Note:**_ 

- `6` _When the term “I3C Specification” is used in reference to_ _**[MIPI06]** in this Application Note, it means_ `7` _the current state of I3C in a generic sense (i.e., the most recently adopted version of either the I3C_ `8` _Specification or the I3C Basic Specification)._ 

- `9` 

   - I3C’s main features include: 

- `10` • Support for lower voltage: 1.2V for typical applications, and down to 1.0V in I3C Basic 

- `11` • Dynamic Addressing assignment 

- `12` • High Data Rate (HDR) Modes with reduced energy requirements 

- `13` • Multi-Controller and Multi-Drop capabilities 

- `14` • In-Band Interrupts 

- `15` 

   - Hot-Join support 

- `16` • Backward compatibility with I²C 

`17` The I3C interface plays a fundamental role in streamlining sensor integration in smartphones, wearables, `18` and Internet-of-Things (IoT) devices. The I3C interface is also extensible to newer and more advanced use `19` cases that go beyond the original scope of sensor integrations. 

`20` This Application Note is intended to help users understand how the I3C interface works, by presenting a `21` range of topics that are relevant for platform architects, HW designers, system integrators, SW developers, `22` and other engineers who enable and support systems that use I3C Buses. 

## `23` **1.1 Scope** 

- `24` 

- `25` 

- `26` 

This General Topics Application Note is intended to guide several different groups: 

   - Those developing MIPI I3C Controller and Target Devices to understand how their parts will fit into different types of systems, and the considerations for functionality and features. 

- `27` • System Designers who need to design systems that integrate such I3C Devices, and potentially `28` Legacy I[2] C Devices, and who need to know considerations of trace layout and connections, `29` voltage regulation for the Devices, any strapping or other ID factors, etc. 

- `30` • MIPI I3C Controller SW developers, including those who must pay special consideration to `31` systems with multiple I3C Controllers on the same I3C Bus. This includes users of both `32` standardized Host Controller APIs and MCU/DSP firmware. 

`33` This Application Note has several parts, each focusing on a different area and covering both required `34` considerations and optional ones, based on which features and topology are used in a given system. This `35` approach makes it easier for any of the targeted groups to focus on what matters to them based on what `36` configurations they will be working with. 

`37` This Application Note is intended to be used together with the latest I3C Specification _**[MIPI06]**_ . Each `38` Application Note section corresponds to one or more Specification sections, primarily focusing on `39` Specification _**Section 6, I3C Electrical Specifications**_ . The Application Note sections amplify the `40` Specification with additional context (e.g., analysis data to back up recommended use models) and details `41` (e.g., total Bus capacitance vs. per-Device capacitance allowances) that might not be presented in the `42` protocol specification itself. 

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

App Note for I3C: General Topics 

App Note Version 1.1 27-Apr-2022 

## `43` **2 Terminology** 

- `44` See also _**Section 2**_ in the MIPI I3C Specification _**[MIPI06]**_ 

## `45` **2.1 Definitions** 

- `46` **System Designer:** Engineer designing a system that includes an I3C Bus. 

## `47` **2.2 Abbreviations** 

- `48` e.g. For example (Latin: exempli gratia) 

- `49` i.e. That is (Latin: id est) 

## `50` **2.3 Acronyms** 

- `51` CCC Common Command Code 

- `52` HDR High Data Rate 

- `53` HJ Hot-Join 

- `54` I3C MIPI Improved Inter Integrated Circuit interface, or its Specification document _**[MIPI06]**_ `55` IBI In-Band Interrupt `56` SDR Single Data Rate 

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

2 

App Note Version 1.1 27-Apr-2022 

App Note for I3C: General Topics 

## `57` **3 References** 

- `58` [MIPI01] _MIPI Alliance Specification for I3C® (Improved Inter Integrated Circuit)_ , version 1.0, `59` MIPI Alliance, Inc., 23 December 2016 (MIPI Board Adopted 31 December 2016). `60` [MIPI02] _MIPI Alliance Specification for I3C (Improved Inter Integrated Circuit)_ , version 1.1 `61` incorporating Errata 01, MIPI Alliance, Inc., 27 December 2019 (MIPI Board Adopted `62` 11 December 2019); Errata 01 approved 24 June 2020. `63` [MIPI03] _MIPI Alliance Specification for I3C (Improved Inter Integrated Circuit)_ , version 1.1.1, `64` MIPI Alliance, Inc., 11 June 2021 (MIPI Board Adopted 8 June 2021). `65` [MIPI04] _MIPI Alliance Specification for I3C Basic[SM] (Improved Inter Integrated Circuit – Basic)_ , `66` version 1.0, MIPI Alliance, Inc., 19 July 2018 (MIPI Board Adopted 8 October 2018). `67` [MIPI05] _MIPI Alliance Specification for I3C Basic℠ (Improved Inter Integrated Circuit – Basic)_ , `68` version 1.1.1, MIPI Alliance, Inc., 9 June 2021 (MIPI Board Adopted 23 July 2021). `69` [MIPI06] Either _**[MIPI03]**_ or _**[MIPI05]**_ . `70` _**Note:**_ `71` _When the term “I3C Specification” is used in reference to_ _**[MIPI06]** , it means the_ `72` _current state of I3C in a generic sense (i.e., the most recently adopted version_ `73` _of either the I3C Specification or the I3C Basic Specification)._ `74` [MIPI07] MIPI Alliance, Inc., “Current I3C Device Characteristic Register (DCR) Assignments”, `75` <https://www.mipi.org/MIPI_I3C_device_characteristics_register>, `76` last accessed 27 July 2022. `77` [MIPI08] _MIPI Alliance I3C Application Note: Virtual Devices and Virtual Targets_ , App Note `78` version 1.0, MIPI Alliance, Inc., 30 August 2021 (MIPI Board Approved `79` 4 September 2021). `80` [MIPI09] _MIPI Alliance I3C Application Note: Hot-Join_ , App Note version 1.0, `81` MIPI Alliance, Inc., 30 August 2021 (MIPI Board Approved 4 September 2021). `82` [MIPI10] _MIPI Alliance Conformance Test Suite for I3C v1.1.1 and I3C Basic v1.1.1_ , `83` CTS version 1.0, MIPI Alliance, Inc., 4 August 2021 (MIPI Board Approved `84` 5 August 2021). `85` [NXP01] UM10204, _I2C-bus specification and user manual_ , Rev. 7.0, NXP Semiconductors, `86` 1 October 2021. 

Copyright © 2018–2022 MIPI Alliance, Inc. 

3 

**Public Release Edition** 

App Note for I3C: General Topics 

App Note Version 1.1 27-Apr-2022 

This page intentionally left blank. 

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

4 

App Note Version 1.1 27-Apr-2022 

App Note for I3C: General Topics 

## `87` **4 Overview** 

- `88` This Application Note describes two broad categories of information: 

- `89` • Details of a few typical and supported topologies, including different trace distances. This covers `90` the allowances and challenges presented by each topology. 

- `91` • Details of added functionality and allowances, including Hot-Join and Hot-insertion, Timing `92` control (timestamping) considerations, power states of Devices and the implications for the Bus, `93` etc. 

## `94` **4.1 Supported Topologies** 

- `95` This Application Note provides additional guidance not found in the I3C Specification itself _**[MIPI06]**_ `96` System Designers who are developing I3C-based systems are encouraged to consult the sections that are `97` relevant to their designs. 

- `98` Analysis data is provided to help understand the considerations that impact the placement and usage of `99` mixed Devices. This analysis data can also be extrapolated to other configurations. It could be used, for 

- `100` example, when choosing what types of Devices to mix on one Bus with a given topology (e.g., single Bus `101` configuration vs. two-Bus configuration), when deciding how best to manage relative Device locations `102` (floor-planning), and when gauging system reliability. 

## `103` **4.2 Using Added Functionality** 

- `104` The I3C Specification _**[MIPI06]**_ includes optional advanced capabilities and features, giving the System `105` Designer the flexibility to choose which ones to use for a particular implementation. Many of these features `106` allow for efficient implementations that can be applied to diverse use cases. The choice of added features `107` may have implications for the System Designer, and for software on the Controller (i.e., on the Host). 

`108` The I3C Specification provides an exact and detailed description of how each feature works with the I3C `109` protocol. The specification is quite extensive, as it includes numerous possible configurations and special `110` cases, and as a result can be challenging for new readers to absorb. By contrast, this Application Note is `111` more descriptive and provides additional information on how the features can be incorporated into a `112` system. System Designers can use this additional information for easier, faster assessment of whether the `113` features are applicable for their designs. 

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

App Note for I3C: General Topics 

App Note Version 1.1 27-Apr-2022 

This page intentionally left blank. 

6 

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

App Note Version 1.1 27-Apr-2022 

App Note for I3C: General Topics 

## `114` **5 System Integration Guidelines** 

`115` This section discusses key guidelines that system integrators will want to follow in their designs, with the `116` goal of optimizing an I3C Bus for various topologies. These are intended either for Pure Bus configurations `117` (i.e., Buses with only I3C Devices), or for Mixed Bus configurations (Buses with both I3C Devices and `118` Legacy I[2] C Devices). 

- `119` 

```
120
```

The guidelines focus on: 

   - I3C Bus Operation 

- `121` • I3C Device Characteristics 

- `122` • Legacy I[2] C Device Characteristics 

- `123` • Dynamic Address Assignment 

- `124` • Bus Topologies 

- `125` 

   - Physical/Electrical/Testing Considerations (CTS) 

- `126` • Bus High Keeper feature 

```
127
```

## **5.1 I3C Bus Operation** 

`128` An I3C Bus operates with an active Controller and one or more Targets, exchanging data using two lines, `129` SDA and SCL, with many similarities with the I[2] C bus _**[NXP01]**_ . Controllers and Targets have a number of `130` types and roles as detailed in _**Section 5.2.1**_ of this Application Note, _**Devices Roles and Responsibilities**_ . 

`131` The Bus begins operation in the default SDR Mode (Single Data Rate, see specification _**Section 5.1**_ `132` _**[MIPI06]**_ ) where data clocking shares many similarities with I[2] C. During a Bus Transaction, the Bus may `133` switch into one of the HDR Modes described later. 

- `134` In SDR Mode, the meaning and operation of the SDA and SCL lines are: 

- `135` • **SCL:** The **S** erial **CL** ock line is the used by the Controller to clock data on the SDA line. SCL is `136` driven by the Active Controller in Push-Pull mode, with a typical 4 mA drive strength, which `137` results a reasonable transition time for a Bus configuration up to 50 pF Bus capacitance. 

- `138` • **SDA:** The **S** erial **DA** ta line mostly carries data in/out, and is also used for additional signaling `139` purposes. Unlike SCL, SDA can be driven either by the Active Controller or by a Target. SDA can `140` operate in either Open Drain or Push-Pull configuration, depending on the Bus state during Bus `141` transactions. 

`142` During the SDR data shifting operation, SDA can change state only when SCL is low. The bit value is `143` latched following the SCL rising edge; see _**Figure 235**_ and _**Figure 236**_ from the I3C Specification `144` _**[MIPI03]**_ ( _**Figure 146**_ and _**Figure 147**_ from the I3C Basic Specification _**[MIPI05]**_ ) for data set-up and `145` holding times. The SDA/SCL line operation changes when the Bus enters into one of the HDR Modes `146` (High Data Rate) where SCL/SDA are operated differently, as explained below in _**Section 5.1.4**_ of this `147` Application Note, _**High Data Rates (HDR Modes)**_ . 

`148` I3C Bus transactions are delimited by the same START (S), Repeated START (Sr), and STOP (P) `149` conditions that I[2] C uses. 

- `150` 

The timing specifications are defined for three different operating conditions: 

- `151` • **I3C is in Open Drain state** per _**Table 122**_ in the I3C Specification ( _**Table 86**_ in the I3C Basic `152` Specification) 

- `153` • **I3C is in Push-Pull state** , covering the SDR, HDR-DDR, and HDR-BT Modes per _**Table 123**_ in `154` the I3C Specification ( _**Table 87**_ in the I3C Basic Specification) and HDR-TSP and HDR-TSL `155` Modes as per _**Table 124**_ in the I3C Specification. 

- `156` • **I3C is communicating with I[2] C Legacy Device(s)** , per _**Table 121**_ in the I3C Specification ( _**Table**_ `157` _**85**_ in the I3C Basic Specification) 

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

App Note for I3C: General Topics 

App Note Version 1.1 27-Apr-2022 

- `158` Care must be taken because most of the timing parameters, such as rise/fall time, data set-up, etc., will be `159` different for the three operating conditions that will change dynamically. 

## `160` **5.1.1 Format of Data Transfer Units** 

`161` A Bus transmission is done by sending 9-bit sequences. A sequence can be either Control or Data. One or `162` more Control sequences are sent first, then Data sequences may follow. 

`163` • **Control Sequence format:** 

- `164` • Either a **7-bit Address** or a **Command Code** , issued by the Controller. 

```
165
```

   - **RnW bit:** 1=Read, 0=Write, issued by the Controller. 

- `166` • **ACK bit:** 0=ACK, 1=NACK (i.e., not-ACK). Emitted by one or more Targets. 

`167` _**Note:**_ 

`168` _During the ACK period, the SDA is always put in Open Drain to allow multiple_ `169` _targets to pull SDA low to signal the ACK. In some special cases (for example, In-_ `170` _Band Interrupt and Hot-Join), the Active Controller may also ACK._ 

`171` • **Data Sequence:** 

```
172
```

   - **8-bit Data:** Read or Write, depending on the RnW bit of the previous Control Sequence. 

- `173` • **9[th] bit:** The meaning of this bit differs between Read transfers and Write transfers: 

- `174` • **During Writes** the 9[th] bit indicates the parity of the Data, as an integrity check (using odd `175` parity) 

- `176` • **During Reads** the 9[th] bit is called **Transition Bit or T-Bit** , and it tells the Controller whether `177` the Target has more data to send: if the T-Bit is 1, then the Target has more data to send; if 0, `178` then there’s no more data to send. 

- `179` For Reads, the Target switches the SDA line to Hi-Z on the raising edge of the SCL `180` signal. This allows the Controller to either continue or stop the transfer by issuing a `181` STOP (i.e., holding and then raising SDA) or a Repeated START. 

`182` For complete details regarding T-Bit operation, see I3C Specification _**Section 5.1.2.3.3**_ `183` and _**Section 5.1.2.3.4 [MIPI06]**_ . 

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

8 

App Note Version 1.1 27-Apr-2022 

App Note for I3C: General Topics 

## `184` **5.1.2 Bus Transfers** 

- `185` In I3C a Controller initiates Bus Transfers, except for a few special cases such an In-Band Interrupt or Hot- 

- `186` Join. Controller-initiated Bus Transfers always start with the I3C Reserved Address, whose value 7’h7E is `187` ignored by I[2] C Targets. This makes it possible to detect whether there are any I3C Targets active on the `188` Bus, and if so, to then switch to Push-Pull mode for a more efficient transfer. 

- `189` I3C extends I[2] C’s basic Read and Write concepts by adding commands, called Common Command Codes `190` (CCC) which may or may not have an associated Data Sequence. Immediately following the Reserved `191` address ACK, a CCC is sent, possibly followed by Data Sequence. 

- `192` _**Figure 1**_ ’s first three illustrations (A, B, and C) show the three currently defined types of CCC Bus `193` transfers: 

- `193` 

- `194` • **A: Broadcast CCC Writes** perform a Write to all Targets that are active on the bus. 

- `195` 

   - **B: Directed CCC Writes** perform a Write to a single addressed Target. 

- `196` • **C: Directed CCC Reads** perform a Read from a single addressed Target. 

- `197` _**Note:**_ 

`198` _A rapid succession of Reads or Writes addressing different Targets can be executed by using_ `199` _Directed CCCs separated only by Repeated STARTs._ 

- `200` Sending a Directed CCC is not the only option to exchange data. I3C can also perform unstructured Write `201` and Read transfers, called Private Transfers, where the data content is application specific. 

- `202` Private Transfers take place after the Reserved byte 7’h7E with RnW=0, followed by a Repeated START. `203` The Target Address is sent with a RnW bit properly set (see _**Figure 1**_ illustrations D and E): 

- `204` • **D: Private Write** transfer if RnW=0, followed by Data Sequence sent by the Controller, with `205` T=odd parity. 

- `206` • **E: Private Read** transfer if RnW=1, followed by Data Sequence sent by the Target, until T=0 (no `207` more data). 

- `208` 

- As the above makes clear, I3C Bus transfers are more complex than those in I[2] C. 

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

App Note for I3C: General Topics 

App Note Version 1.1 27-Apr-2022 

## **A: I3C Broadcast CCC Write** 

**==> picture [456 x 138] intentionally omitted <==**

**----- Start of picture text -----**<br>
S orSr I3C Reserved Byte(7'h7E) (RnW=0) ACK Broadcast CCC(0x00 to 0x7F) T=p Write Data-1Optional T=p ... Write Data-NOptional T=p or PSr<br>B: I3C Directed CCC Write –  More than one Target possible<br>S orSr I3C Reserved Byte(7'h7E) (RnW=0) ACK (0x80 to 0xFE)Directed CCC T=p Sr<br>Target 1 Address(RnW=0) ACK Write Data-1Optional T=p ... Write Data-NOptional T=p Sr, 7'h7E, or P<br>Target 2 Address(RnW=0) ACK Write Data-1Optional T=p ... Write Data-NOptional T=p Sr, 7'h7E, or P Repeatas needed<br>**----- End of picture text -----**<br>


- **C: I3C Directed CCC Read –** More than one Target possible 

**==> picture [563 x 236] intentionally omitted <==**

**----- Start of picture text -----**<br>
S orSr I3C Reserved Byte(7'h7E) (RnW=0) ACK (0x80 to 0xFE)Directed CCC T=p Sr<br>Target 1 Address ACK Read Data-1 T=1 ... Read Data-N T=0 Sr, 7'h7E,<br>(RnW=1) or P<br>Target 2 Address ACK Read Data-1 T=1 ... Read Data-N T=0 Sr, 7'h7E,  Repeat<br>(RnW=1) or P as needed<br>D: I3C Private Write Transfer<br>S orSr I3C Reserved Byte(7'h7E) (RnW=0) ACK Sr Target Address(RnW=0) ACK Data-1Write T=p ... Write Data-N T=p or PSr<br>E: I3C Private Read Transfer<br>S or I3C Reserved Byte ACK Sr Target Address ACK Read T=1 ... Read Data-N T=0 Sr<br>Sr (7'h7E) (RnW=0) (RnW=1) Data-1 or P<br>LEGEND tsco Controller toTarget Target toController T=p Controller to TargetT-Bit = Data Byte Parity T=1 Target to ControllerT-Bit = 1 (More Data) T=0 Target to ControllerT-Bit = 0 (No More Data)<br>**----- End of picture text -----**<br>


**Figure 1 I3C Transfer Types** 

```
209
```

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

10 

App Note Version 1.1 27-Apr-2022 

App Note for I3C: General Topics 

## `210` **5.1.3 SDA Line Discipline** 

- `211` I3C Controller and Target Devices must be able to dynamically switch the SDA line between Open Drain, `212` Hi-Z, and Push-Pull configurations. During Bus idle, the SDA line is in Hi-Z to allow targets to initiate In- `213` Band Interrupts, Hot-Join events, or Secondary Controller Requests. Following the START condition, `214` during the initial 7-bit address (for the I3C Reserved Address 7’h7E, the IBI reserved address, or other `215` address values) the SDA must be kept in Open Drain to allow address arbitration to occur. After the `216` arbitration is concluded, SDA can be switched into Push-Pull, driven by either the Controller or the Target, `217` depending on the Bus transfer stage. 

- `218` 

Additionally, there are a few conditions where SDA must be kept in Open Drain or Hi-Z mode: 

- `219` • During Dynamic Address Assignment (DAA), the 48-bit unique ID is issued in Open Drain mode `220` to allow arbitration. DAA will occur at Bus initialization, or during a Hot-Join Request. 

   - During ACK bit time, to detect whether any Targets (i.e., at least one Target) is issuing an ACK. 

- `221` 

- `222` • In a Read, during T-Bit time after the SCL raising edge, to allow the Controller to either continue `223` or abort the transfer. 

- `223` 

- `224` • During a Secondary Controller Request to become the Active Controller, to allow address `225` arbitration in case of requests collision. 

## `226` **5.1.4 High Data Rates (HDR Modes)** 

- `227` In addition to Standard Data Rate (SDR) Mode, I3C also supports data transfer at higher speeds through the `228` use of more sophisticated line coding, and/or multiple (x2 or x4) SDA lanes. 

- `229` There are currently four supported HDR Modes. 

- `230` 

Two HDR Modes are available in both the full I3C Specification and I3C Basic: 

- `231` • **HDR-DDR Mode:** Double Data Rate, where data bits are clocked on every SCL edge transition (i.e., `232` both the rising edge and the falling edge), effectively doubling SDR Mode data rate. 

- `233` • **HDR-BT Mode:** Bulk Transport, an SDR-like mode that is block oriented, using the 9[th] bit for data `234` instead of the usual Parity or T-Bit function (data integrity is checked with CRC instead). This results `235` in a 20% performance gain over the base SDR Mode. 

- `236` 

The two Ternary Modes are only available in the full I3C Specification, not in I3C Basic: 

- `237` • **HDR-TSP Mode:** Ternary Symbol, Pure Bus, where SDA and SCL lose their ordinary functions and `238` data is instead sent over both wires in the form of ternary symbols, achieving x3 speed gain. HDR-TSP `239` Mode is not compatible with Legacy I[2] C Devices, so it requires a ‘pure’ I3C Bus (only I3C Devices, no `240` Legacy I[2] C Devices). 

- `241` • **HDR-TSL Mode:** Ternary Symbol, Legacy Bus. Similar to HDR-TSP Mode, but allows Legacy I[2] C `242` Devices to be present on the Bus. This comes at the cost of a slight performance reduction compared to `243` HDR-TSP Mode: x2.5 speed gain, instead of 3x. 

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

App Note for I3C: General Topics 

App Note Version 1.1 27-Apr-2022 

## `244` **5.2 I3C Device Characteristics** 

- `245` Devices on an I3C Bus have different Roles, each bearing distinct responsibilities. 

`246` The defined Roles are: 

- `247` • Primary Controller 

- `248` • Secondary Controller 

- `249` • Target 

- `250` • SDR-Only Primary Controller 

- `251` • SDR-Only Secondary Controller 

- `252` • SDR Only Target 

- `253` An active I3C Device playing a given Role in a given I3C Bus instantiation will fulfill all responsibilities `254` for that Role, as detailed in the I3C Specification at _**Section 4.2**_ ( _**Table 1 Roles for I3C Compatible**_ `255` _**Devices**_ ) and _**Section 5.1.1.1**_ ( _**Table 2 Devices Roles vs Responsibilities**_ ) _**[MIPI06]**_ . 

- `256` A given I3C Device may perform different Roles at different times. The most notable cases of this are (A) a `257` Target that gains a Secondary Controller Role to accomplish a specific task, and then relinquishes the Role `258` after completing the task, and (B) when an I3C Target Device connects after initialization (i.e., the Hot-Join `259` Request), which may also change the electrical characteristics of the I3C Bus. 

- `260` As a result, the configuration of a given I3C Bus can vary over time: it will depend upon the Roles and the `261` states of the I3C Devices that are active on that I3C Bus at a given time. System Designers should `262` anticipate these dynamic changes in the configuration of the I3C Bus, and account for them in their designs. 

- `263` Device Roles are grouped into two sets, based on whether the Device supports HDR Mode. As the names `264` imply, the SDR-Only Devices cover the Roles of I3C Devices that do not support any of the HDR Modes. `265` By contrast, the Devices in the Roles of Primary Controller, Secondary Controller, and Target may choose `266` which of the optional HDR Modes to support. 

- `267` _**Note:**_ 

- `268` _I3C Devices that are not HDR capable (or that only support some HDR Modes) are required (A) to_ `269` _be tolerant of the HDR Modes that they do not support, and (B)to recognize the HDR Exit Pattern._ 

- `270` _SDR-Only Primary Controller Devices and SDR-Only Secondary Controller Devices are still_ `271` _required to support and use the HDR Exit Pattern, for certain error recovery situations. For details,_ `272` _see the I3C Specification at_ _**Section 5.1.10 [MIPI06]** ._ 

`273` _For the remainder of this Application Note, the differences between a Role and its SDR-Only_ `274` _counterpart will not generally be relevant; as such, the Roles of Primary Controller, Secondary_ `275` _Controller and Target are used in most situations where HDR Mode support is not relevant to a_ `276` _particular section._ 

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

12 

App Note Version 1.1 27-Apr-2022 

App Note for I3C: General Topics 

## `277` **5.2.1 Devices Roles and Responsibilities** 

## `278` **5.2.1.1 Primary Controller Role** 

`279` In an I3C Bus there can be only one Primary Controller Device. The Device designated as the Primary `280` Controller keeps its Role at all times, even when it is not the Active Controller of the I3C Bus. 

- `281` _**Note:**_ 

`282` _If the Primary Controller supports only SDR data transport, then it is referred as an SDR-Only_ `283` _Primary Controller. This Application Note will generically refer to the term Primary Controller, unless_ `284` _the “SDR-Only” qualifier is needed._ 

`285` The Role of Primary Controller is the most complex in the I3C Bus. The Primary Controller has the `286` authority for the initial configuration of the Bus and all Devices, including any Legacy I[2] C Devices. It must `287` be capable of handling all Bus Configuration procedures. 

- `288` 

The required capabilities of the Primary Controller include: 

- `289` • Assign Dynamic Addresses using the ENTDAA, SETDASA, and SETAASA CCCs (per the I3C `290` Specification at _**Section 5.1.4 [MIPI06]**_ ) to: 

- `291` • All I3C Targets, as part of Bus Initialization and any subsequent Bus Configuration, and to itself 

- `292` 

   - Any Hot-Joining Devices that might not be present during Bus Initialization 

- `293` • Maintain a memory map of assigned Dynamic Addresses for all I3C Targets, including their Bus `294` Characteristics and configuration (i.e., BCR and DCR) 

- `295` • Manage the SDA and SCL Bus Lines while serving as the Active Controller, including: 

   - In SDR, HDR-DDR and HDR-BT Modes, driving the SCL line for data clocking 

- `296` 

- `297` • During the I3C Address Header, manage Address Arbitration per _**Section 5.1.2.2**_ of the I3C `298` Specification _**[MIPI06]**_ , especially when starting new transfers with the 7’h7E Broadcast `299` Address 

- `299` 

- `300` • Generate the SDA ACK during a Hot-Join Request per _**Section 5.1.5**_ of the I3C Specification `301` _**[MIPI06]**_ , and during an In-Band Interrupt Request per _**Section 5.1.6**_ , as and when the Primary `302` Controller is enabled to support such interrupts 

- `303` 

   - HDR Mode management 

- `304` • Support data reception for read transfers in the optional HDR-TSP and/or HDR-TSL Modes, `305` i.e., when passing control of both SDA and SCL to a particular I3C Target) 

- `306` • Generate the I3C Target Reset Pattern, per _**Section 5.1.11**_ of the I3C Specification _**[MIPI06]**_ 

`307` If the I3C Bus also contains one or more Secondary Controller Devices, then the Primary Controller is `308` required to have additional capabilities: 

- `309` 

   - Respond to Controller Role Requests from a Secondary Controller 

- `310` • Pass the Controller Role to a chosen Secondary Controller, per _**Section 5.1.7.2**_ of the I3C `311` Specification _**[MIPI06]**_ : 

- `312` 

   - Prepare the Bus for Handoff 

- `313` • Use the defined Controller-to-Controller Handoff Procedure to transfer the Controller Role 

- `314` • After passing the Controller Role, remain in standby mode (the behavior is similar to a Secondary `315` Controller) while the other Controller-capable device holds the Active Controller Role, until it is `316` time to pass the Controller Role back again 

- `317` • Transfer the assigned Dynamic Address memory map to any Secondary Controller Devices that `318` might be on the Bus. This includes Group Address assignment for any I3C Targets that are `319` members of Groups. 

Copyright © 2018–2022 MIPI Alliance, Inc. 

13 

**Public Release Edition** 

App Note for I3C: General Topics 

App Note Version 1.1 27-Apr-2022 

## `320` **5.2.1.2 Secondary Controller and SDR-Only Secondary Controller Roles** 

- `321` In I3C, a Target can also hold the Role of Secondary Controller. For that, the Device should be capable of `322` requesting and/or acquiring the Controller Role, i.e., of becoming the Active Controller. The Controller `323` Role can only be passed after the Primary Controller has performed Bus Initialization. 

- `324` The I3C Specification does not place any time limitation on when a Secondary Controller can become the `325` Active Controller of the Bus, however, it is expected that for most applications, a Secondary Controller will `326` remain Active only for the amount of time needed to perform a specific task. Once the task is complete, the `327` Secondary Controller will relinquish the Active role, usually back to the Primary Controller, or potentially `328` to another Controller-capable Device on the I3C Bus (the actual behavior will depend on the particular `329` application). 

- `330` Controller-capable Devices use the Controller-to-Controller Handoff Procedure that is managed by the `331` current Active Controller, as described in _**Section 5.1.7.2**_ of the I3C Specification _**[MIPI06]**_ . Note that this `332` Controller-to-Controller Handoff Procedure is the only means by which an Active Controller can hand the `333` Controller Role off to another Controller-capable Device (e.g., a Secondary Controller). 

- `334` _**Note:**_ 

- `335` _The Controller-to-Controller Handoff Procedure always has the same flow, no matter whether the_ `336` _Active Controller is the Primary Controller at Bus Initialization time vs. a Secondary Controller._ 

- `337` _It is important to understand that I3C Controller-capable Devices do not directly contend with one_ `338` _another for the Controller Role. Instead, the Controller-to-Controller Handoff Procedure is fully_ `339` _managed by the Active Controller, using the GETACCCR CCC per I3C Specification_ `340` _**Section 5.1.9.3.16 [MIPI06]** ._ 

- `341` The responsibilities of an Active Secondary Controller are similar to those of the Primary Controller: 

- `342` • Manage the SDA and SCL Bus Lines while serving as the Active Controller 

- `343` • Optionally Assign Dynamic Addresses to a Hot-Joining Device, using the ENTDAA CCC 

- `344` • Receive and maintain a memory map of assigned Dynamic Addresses for some or all I3C Targets, `345` including their characteristics and configuration (i.e., BCR and DCR) 

- `346` • If the assigned Dynamic Address memory map has changed while this Device was the Active `347` Controller, then transfer the updated memory map to the Primary Controller 

- `348` A Secondary Controller is also required to be capable of interacting with the Primary Controller and any `349` other Controller-capable Devices: 

- `350` • If the assigned Dynamic Address memory map has changed while this Device was the Active `351` Controller, then transfer the updated memory map to any other Secondary Controller Devices and `352` the Primary Controller. This includes changes to Group Addresses if any of them have changed. 

- `353` • Respond to any Controller Role Requests that are received from Controller-capable Devices on the `354` Bus (including the Primary Controller) 

- `355` • Pass the Controller Role to a chosen Controller-capable Device, per the I3C Specification at `356` _**Section 5.1.7.2 [MIPI06]**_ : 

- `357` • Prepare the Bus for Handoff 

- `358` • Use the defined Controller-to-Controller Handoff Procedure to transfer the Controller Role 

- `359` • After passing the Controller Role, remain in standby mode (i.e., act only as a Secondary `360` Controller) while the other Controller-capable Device holds the Active Controller role, until `361` such time as the Controller Role is passed back again. 

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

14 

App Note Version 1.1 27-Apr-2022 

App Note for I3C: General Topics 

## `362` **5.2.1.3 Target and SDR-Only Target Role** 

`363` Since I3C transactions are initiated by the Active Controller, the Role of I3C Target Devices is for the most `364` part a passive one. 

`365` However, there are a few instances in which a Target plays an active role, generating signals to initiate `366` specific actions: 

- `367` • To initiate an In-Band Interrupt request, a Target can pull the SDA line low (see the I3C `368` Specification at _**Section 5.1.6 [MIPI06]**_ ). 

- `369` • To initiate a Hot-Join Request, a Target can pull the SDA line low (see the I3C Specification at `370` _**Section 5.1.5 [MIPI06]**_ ). 

- `371` • A Target also manages the T-Bit: 

- `372` • For Writes, the T-Bit indicates parity from the Active Controller 

- `373` • For Reads, the Target uses the T-Bit to indicate whether additional data bytes are available: if the `374` Active Controller drives the T-Bit to 0, then the Target will end the Read transfer. 

- `375` If a Target is HDR-capable, then it is also required to: 

- `376` • Support the appropriate ENTHDRx CCC to enter the HDR Mode, per the I3C Specification at `377` _**Section 5.1.9.3.9 [MIPI06]**_ 

- `378` • Recognize its assigned Address in the appropriate manner (i.e., a Command Word or Header `379` Block, specific to the HDR Mode) and respond appropriately when the Address matches (i.e., `380` providing ACK or NACK to the command) 

- `381` • Support reception and generation of the different HDR signaling modes, for Write and Read `382` commands initiated by the Active Controller 

- `383` • Detect errors in transmission 

```
384
```

- Recognize the HDR Exit Pattern 

15 

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

App Note for I3C: General Topics 

App Note Version 1.1 27-Apr-2022 

## `385` **5.2.2 Clock-to-Data Turnaround Time (tSCO)** 

`386` This section discusses the impact of Clock-to-Data turnaround (tSCO) on a single-ended, single-clock Bus `387` such as I3C when operating the interface over long traces (> 0.5 m). _**Figure 2**_ illustrates this scenario. `388` Ideally, there should be no timing skew between t3 and t7. To limit this timing skew, the SCL and SDA paths `389` should be designed to be as similar to each other as possible. 

**==> picture [416 x 171] intentionally omitted <==**

**----- Start of picture text -----**<br>
I3C Controller Device I3C Target Device<br>PHY Layer PHY Layer<br>D Q t1 PAD t2 t3 PAD t4 D Q<br>Clock<br>SCL<br>Q D t9 PAD t8 t7 PAD t6 Q D<br>iData<br>SDA<br>t5 = tSCO<br>**----- End of picture text -----**<br>


- t1: Time from Clock Flop Q to Pad 

- t2: Time through output pad (PFET/NFET) 

- (tested over 90        pF line C) 

- t3: Time over wires pad-pad: Controller drive + Line Cap + Tpath 

- t4: Time through input pad of Target 

- t5: Time inside Target, from SCL input to SDA out (tSCO) 

```
390
```

```
391
```

```
392
```

- (to gate drive of SDA) 

**LEGEND Internal delay (excluding pads) PAD delays on a standard Bus model** 

- t6: Time through output pad of Target 

- t7: Time over wires pad-pad: Target drive + Line Cap + Tpath 

- t8: Time through iData input pad (Schmitt input) 

- t9: Time from iData pad to D input for serializer 

## **Figure 2 Components of Clock-to-Data Turnaround Delay (tSCO)** 

## _**Note:**_ 

`393` _**Figure 2** also appears in_ _**Section 5.1.9.3.18** of the I3C Specification_ _**[MIPI06]** where the_ `394` _GETMXDS CCC is defined. GETMXDS allows an I3C Target to return its expected t5 time._ 

## `395` **5.2.3 Pad Capacitance** 

`396` The pad capacitance adds to the capacitance of the Bus wires, and must be considered when computing the `397` effective Bus frequency or other Bus parameters. A Device’s pad capacitance also contributes directly to the `398` skew of the signals, to the Device internal delay, and to the tSCO. For this reason, tSCO was characterized on a `399` standard 50 pF, 90 Ω internal driver resistance. 

## `400` **5.2.4 Pad Drive Strength** 

`401` The pad drive strength is another factor contributing to signal skew, and to the Device’s ability to drive the `402` pad within the required rise and fall time. The minimum recommended Bus drive strength is 4 mA drive. `403` Greater drive strength can be implemented, as long as the Bus reflections and the power requirements of `404` the system design are not affected. Most Bus timing parameters in the I3C Specification were determined `405` using 4 mA drive strength as the measurement reference. When choosing greater drive strength, care must `406` be taken to avoid overshoot. 

16 

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

App Note Version 1.1 27-Apr-2022 

App Note for I3C: General Topics 

## `407` **5.2.5 BCR Use** 

`408` Each I3C Device that is connected to the I3C Bus has an associated read-only Bus Characteristics Register `409` (BCR). The BCR fields describe the Device’s Role and capabilities that Primary and Secondary Controllers `410` must consider when operating a Device on the Bus. The BCR is described in the I3C Specification at `411` _**Section 5.1.1.2.1**_ , in _**Table 5 Bus Characteristics Register [MIPI06]**_ , reproduced below as _**Figure 3**_ (table `412` notes omitted). 

`413 414` 

## **Figure 3 Bus Characteristics Register (BCR)** 

- If **BCR bit [0]** is set, then one or more of the following limitations apply: 

`415`  **BCR bit [0]** `416` • The Device is not capable of operating at the 12.5 MHz maximum operating frequency `417` • The time between the end of the SCL falling edge and start of the SDA output from the Target is `418` greater than 12 ns `419` • Overall internal Device delays, including Pads (see _**Figure 2**_ ), is greater than 12 ns `420` • The Device requires more time to prepare the requested data. As a result, the Controller will `421` have to send a GETMXDS command to communicate a lower speed that is acceptable by all `422` Devices to determine the particular limitation(s), and then take the appropriate measure(s) `423` necessary to accommodate the Device. 

- The time between the end of the SCL falling edge and start of the SDA output from the Target is greater than 12 ns 

Copyright © 2018–2022 MIPI Alliance, Inc. 

17 

**Public Release Edition** 

App Note for I3C: General Topics 

App Note Version 1.1 27-Apr-2022 

- `424` • **BCR bits[2:1]** are related to In-Band Interrupt. If BCR bit [1] is set, then the Target is capable of `425` issuing IBI Requests. If BCR bit [2] is also set, then during the IBI event the Controller will `426` continue to generate SCL clock pulses to allow the Target to return the IBI Mandatory Data Byte, `427` followed by additional data, until the data transfer is terminated (either terminated by the Target `428` itself via the T-bit, or terminated by the Active Controller). 

- `429` • If **BCR bit [3]** , the Offline Capable bit, is set, then the Device is capable of going offline (i.e., of `430` entering a state in which it will not respond to commands, but still retains its Dynamic Address). 

- `431` • If **BCR bit [4]** , the Virtual Target Support bit, is set, then the Device is capable of presenting `432` multiple Virtual Targets, or capable of exposing other downstream Devices (i.e., from another I3C `433` Bus segment, or from any other Bus type) 

- `434` 

## _**Note:**_ 

- `435` _The meaning of BCR bit [4] has changed from earlier versions of the I3C Specification. For_ `436` _additional requirements for Virtual Target support, see the I3C Specification at_ `437` _**Section 5.1.2.1.2 [MIPI06]** , and the_ _**Application Note for Virtual Devices & Virtual Targets**_ `438` _**[MIPI08]** ._ 

- `439` • If **BCR bit [5]** , the Advanced Capabilities bit, is set, then the Device supports optional advanced `440` capabilities, such as I3C spec supported version, Device-to-Device Transfer, Group Address, `441` Multi-Lane, and others. The Active Controller can discover which of these optional features are `442` supported by using the GETCAPS CCC per the I3C Specification at _**Section 5.1.9.3.19 [MIPI06]**_ . `443` (The complete set of optional features is listed in that section.). 

- `444` _**Note:**_ 

- `445` _The meaning of BCR bit [5] has changed from earlier versions of the I3C Specification._ `446` _Previously, this bit only indicated whether the Device supported any optional HDR Modes._ `447` _Per earlier versions of the I3C Specification, certain SDR-only Devices might return a 1’b0_ `448` _value in this bit. However, the I3C Specification now requires all conforming Targets and_ `449` _Secondary Controller to return a 1’b1 value, as the GETCAPS CCC now requires such_ `450` _Devices to report other advanced capabilities as well as the I3C Version number that is_ `451` _supported. In practice, all new I3C Target and I3C Secondary Controller implementations must_ `452` _return a 1’b1 value, and must support the GETCAPS CCC._ 

- `453` • **BCR bits[7:6]** , the Device Role bits, indicate whether the Device is simply an I3C Target, or whether it `454` also has Controller Role capabilities. 

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

18 

App Note Version 1.1 27-Apr-2022 

App Note for I3C: General Topics 

## `455` **5.3 Dynamic Address Assignment (DAA)** 

`456` I3C device addressing is different from I[2] C, where devices have hardwired addresses that are fixed, or set `457` by pin strapping. In I3C, a device address is dynamically allocated at Bus initialization time when the `458` Primary Controller issues the ENTDAA CCC. Dynamic Addresses (DAs) can also be assigned `459` subsequently (i.e., after the Bus has been initialized) for some specific cases, such as for a Hot-Joining `460` device. A I3C component becomes fully functional only after it has acquired its DA. The pool of Dynamic `461` Addresses is 7-bit wide; more insights on this topic are given below in _**Section 5.3.3**_ of this Application `462` Note, _**Address Assignment Guidance**_ . 

```
463
```

From the system design perspective, I3C’s Dynamic Addressing scheme brings numerous advantages: 

- `464` • SW drivers and application management can be simplified by associating a given Dynamic Address `465` with a logical function (e.g., a magnetometer), rather than with a specific hardware component. 

- `466` • The relatively small address space (7 bits) is not a limitation, as it is tied to Bus functions, not to `467` different vendor HW models. 

- `468` • The short, and therefore fast, 7-bit address is an efficient way to address a Target on a I3C Bus. 

- `469` • The DA value determines the priority ranking in several I3C Bus transactions. For In-Band Interrupts `470` (IBI), a lower DA value has higher priority, hence the DAA strategy regulates the servicing order for `471` concurrent IBI requests. 

`472` The initial assignment of Dynamic Addresses is the duty of the Primary Controller: as soon as the I3C Bus `473` is powered up, the Primary Controller assigns a unique Dynamic Address to each of the connected Targets. `474` The Primary Controller has also a unique position among other possible Controller-capable Devices that `475` might be connected to the Bus: it is constantly informed of the number of connected components and their `476` characteristics. 

## `477` **5.3.1 Dynamic Address Assignment Procedure** 

```
478
```

The Primary Controller starts the DAA procedure once all of the Devices on the I3C Bus are ready. 

`479` The DAA procedure is really a two-step process. First, every static address is mapped to a DA as explained `480` below. Then the Primary Controller performs the actual DAA operation by issuing the ENTDAA CCC with `481` the 7’h7E reserved Broadcast byte, followed by a Repeated START (see _**Figure 4**_ ). 

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

19 

App Note for I3C: General Topics 

App Note Version 1.1 27-Apr-2022 

`482` 

**Figure 4 Dynamic Address Assignment Transaction** 

`483` All I3C Devices that have not yet received their Dynamic Addresses will respond to the ENTDAA CCC `484` sequence by ACKing the reserved byte, and then sending their 48-bit Provisioned ID which is both unique `485` and arbitrable. Although multiple I3C Devices will ACK the CCC, the Primary Controller will only assign `486` a 7-bit DA value to the one with the lowest-value Provisioned ID (this is “winning the arbitration”). The `487` winning Device will then not ACK the next ENTDAA CCC, because then it will have a DA. This `488` assignment cycle is repeated until the Primary Controller receives a NACK to the reserved byte, because `489` that indicates that no further Targets are still requesting a DA. The Dynamic Address Assignment procedure `490` ends with a STOP: a robust signaling condition that all Devices connected to the I3C Bus can easily `491` identify. A higher-level I3C Bus Management layer is responsible for managing the whole operation. 

- `492 493` 

- `494` 

- `495` 

- `496` 

- `497` 

`498` 

Optionally, the Primary Controller can end the Dynamic Address Assignment procedure at any time. To complete the DAA procedure, any Devices that haven’t yet received an assigned I3C Dynamic Address will have to participate in a further Dynamic Address Assignment procedure which the Primary Controller will have to schedule at a later time. 

All the details of the Dynamic Address Assignment (Dynamic Address Assignment) procedure are described in the I3C Specification at _**Section 5.1.4.2 Bus Initialization Sequence with Dynamic Address Assignment [MIPI06]**_ . 

`499` After the initial Bus configuration is completed, the Active Controller can still change a Target’s Dynamic `500` Address using the SETNEWDA CCC per _**Section 5.1.9.3.7**_ of the I3C Specification _**[MIPI06]**_ , if the Target `501` supports this CCC. In addition, the Active Controller will assign a Dynamic Address to each Target that is `502` newly attached to the Bus via a Hot-Join Request. 

Copyright © 2018–2022 MIPI Alliance, Inc. 

20 

**Public Release Edition** 

App Note Version 1.1 27-Apr-2022 

App Note for I3C: General Topics 

## `503` **5.3.2 Dynamic Address Consistency** 

- `504` Secondary Controllers need to be informed of the correspondence between the assigned Dynamic `505` Addresses and their associated Targets. This information can be communicated in two ways: 

- `506` • **Passively:** The Secondary Controller(s) monitor the Dynamic Address Assignment procedure, by `507` snooping the data for the CCC Bus transactions for the RSTDAA, ENTDAA, and/or SETNEWDA `508` CCCs, or 

- `509` • **Actively:** The Primary Controller issues the Broadcast DEFTGTS CCC ( _**Define List of Targets)**_ `510` per _**Section 5.1.9.3.7**_ of the I3C Specification _**[MIPI06]**_ . 

- `511` The passive method has several limitations. It only works if the Secondary Controller is powered and active `512` during Bus Initialization. If there are any Targets that use their I[2] C Static Address as their DA (this is `513` configured via the SETAASA CCC), then the Secondary Controller will not see the I[2] C address (SETAASA `514` has not optional data), and they will remain unknown. Also, if the Secondary Controller goes into an idle or `515` powered-down mode, then it might miss later DAA procedures with the ENTDAA CCC. 

- `516` The active method, though more complex, is more reliable than the passive method. 

## `517` **5.3.3 Address Assignment Guidance** 

- `518` Proper selection and allocation of the Dynamic Addresses is crucial for the functioning of the I3C Bus. `519` Although there is a maximum of 128 possible Dynamic Addresses (because the address is 7 bits wide), in `520` practice the typical number of physical Devices present on a I3C Bus is considerably less than that, partly `521` because the maximum capacitance limit is typically reached well before 128 Devices can be placed on the `522` Bus (i.e., the combined capacitances of the I/O pins and the Bus wiring is 50 pF for a typical system). 

- `523` Note that it is possible for the number of assigned, unique Dynamic Addresses to be greater than the `524` number of Devices physically present on the Bus. This can happen because besides the physical Device `525` addresses, the DA count will also include one additional DA for each Virtual Target (per I3C Specification `526` _**Section 5.1.2.1.2 [MIPI06]**_ ) and one additional DA for each Group Address ( _**Section 5.1.2.1.3**_ ) that those `527` Devices implement. 

## `528` **5.3.3.1 Effective Address Space** 

`529` Though the Dynamic Address is 7 bits wide, the number of usable Dynamic Addresses is less than 128 `530` because several values are either reserved in the I3C protocol, or cannot be used under certain conditions. 

`531` The I3C Specification details the unavailable addresses at _**Section 5.1.2.2.5 I3C Target Address**_ `532` _**Restrictions**_ , but in summary: 

- `533` • The I3C Broadcast Address 7’h7E is not available as a Dynamic Address because in the I3C `534` protocol the 7’h7E value serves as the preamble for virtually all Bus transactions 

- `535` • To make Bus operation more robust against single-bit errors, all addresses that are a 1-bit `536` hamming distance away from the 7’h7E Broadcast Address (i.e., to avoid 1-bit errors) are `537` excluded: 7’h3E, 7’h5E, 7’h6E, 7’h76, 7’h7A, 7’h7C, and 7’h7F 

- `538` • I3C reserves 7’h02 for the Hot-Join address 

- `539` 

- `540` 

- `541` 

   - I3C reserves 7’h00 (its use is forbidden in I3C) 

   - I3C reserves 7’h01 for SETDASA CCC point-to-point communications 

   - If any I[2] C Devices are present on the Bus, then the I[2] C reserved address 7’h03 is excluded 

- `542` • If certain types of Legacy I[2] C Devices are present on the Bus, then the following I[2] C-related `543` addresses are also excluded: 

- `544` 

   - I[2] C Devices supporting High-Speed Mode: 7’h04, 7’h05, 7’h06, 7’h07 

- `545` • I[2] C Devices supporting Extended Address Mode or having an Extended Address: 7’h78, 7’h79, `546` 7’h7B 

- `547` • I[2] C Devices supporting Device ID Mode: 7’h78, 7’h79, 7’h7B 

Copyright © 2018–2022 MIPI Alliance, Inc. 

21 

**Public Release Edition** 

App Note for I3C: General Topics 

App Note Version 1.1 27-Apr-2022 

## `548` **5.3.3.2 Address Allocation Good Practice** 

`549` An optional, but recommended, practice to speed up the Dynamic Address Assignment procedure is to first `550` assign Dynamic Addresses to all Devices with a known Static I[2] C Address via the CCC _**Set Dynamic**_ `551` _**Address from Static Address (SETDASA)**_ ( _**Section 5.1.9.3.10**_ of the I3C Specification). 

`552` Once the Static addresses are set, the actual selection and assignment of Dynamic Addresses takes place. `553` For the following reasons, it is a good practice to leave spaces (i.e., unused addresses) in between the `554` assigned addresses: 

- `555` 

   - To allow for further changes in the priority ranking for In-Band Interrupt (IBI) processing 

- `556` • To reserve pre-interleaved locations for Devices that will Hot-Join the Bus, thus facilitating their IBI `557` priority ranking order. 

`558` As a further option, the Dynamic Addresses can be selected and allocated in the manner described at `559` _**Section 5.1.2.2.2**_ of the I3C Specification, _**I3C Address Arbitration Optimization**_ . The method described `560` there can improve effective data rates by minimizing the amount of time spent in address arbitration `561` operations. 

## `562` **5.3.3.3 Dynamic Address Collision** 

`563` The Dynamic Address Arbitration procedure relies on the I3C Devices on the Bus having a mutually unique `564` 48-bit Provisioned ID. However, since this value is generated using random data, it is possible for two (or `565` more) Targets to independently generate the same Provisioned ID value. Though the probability of this `566` actually occurring is quite small, if it does occur then the Controller will assign the same Dynamic Address `567` to those two (or more) Devices. This is known as an address collision. An address collision might also `568` potentially result if a signal integrity problem causes misreading. 

`569` Detecting whether an address collision has occurred is simple: the total number of I3C Dynamic Addresses `570` actually assigned will be less than the number of Devices known to require a Dynamic Address. 

`571` To recover from an address collision, the Primary Controller may issue the CCC _**Reset Dynamic Address**_ `572` _**Assignment (RSTDAA)**_ (I3C Specification _**Section 5.1.9.3.3**_ ), which causes every I3C Device on the Bus `573` to reset (i.e., to clear) the Dynamic Address it was just assigned. The Controller then re-initiates a new `574` Dynamic Address Assignment procedure, in the hope that the Provisioned IDs will be mutually unique this `575` time. If a collision reoccurs more than a given number of times (three is recommended), then the Primary `576` Controller is required to inform the Application Layer that the I3C Bus is not functional (see the I3C `577` Specification at _**Section 5.1.4.3**_ ). 

## `578` **5.3.3.4 Dynamic Address Modification** 

`579` After the I3C Bus has been successfully configured, the Active Controller can dynamically change assigned `580` Dynamic Addresses as desired for optimal operation of the running application, using the CCC _**Set New**_ `581` _**Dynamic Address (SETNEWDA)**_ (I3C Specification _**Section 5.1.9.3.11**_ ). If any Secondary Controllers are `582` connected to the I3C Bus, then the Active Controller must inform them of any Dynamic Address changes `583` by using the _**Define List of Targets (DEFTGTS)**_ CCC (I3C Specification _**Section 5.1.9.3.7**_ ). 

- `584` 

## _**Note:**_ 

- `585` _Certain I3C Targets might not support the SETNEWDA CCC, and will only support an initially_ `586` _Dynamic Address that cannot be changed after it is assigned (i.e., during Bus Initialization). If such_ `587` _I3C Targets receive their Dynamic Address from their I[2] C Static Address (i.e., using the SETDASA_ `588` _CCC or the SETAASA CCC), then the Dynamic Address is effectively immutable and the Active_ `589` _Controller must manage the assignment of Dynamic Addresses accordingly: for IBI prioritization,_ `590` _the Active Controller must assign Dynamic Addresses for other I3C Targets to work around such_ `591` _immutable Dynamic Addresses for these I3C Targets._ 

- `592` In general, the Active Controller should assign a Dynamic Address to Hot-Joining Targets. However, not all `593` Secondary Controllers are capable of assigning Dynamic Addresses. If a Target attempts to Hot-Join while `594` such a Secondary Controller is the Active Controller, then that Secondary Controller is required to pass the 

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

22 

App Note Version 1.1 27-Apr-2022 

App Note for I3C: General Topics 

`595` Active Controller Role back to the Primary Controller (or to some other Controller known _a priori_ to be `596` sufficiently capable). That new Active Controller will then furnish the Hot-Joining Target with the Dynamic `597` Address it needs, and then inform any other Controller-capable Devices on the Bus (i.e., Secondary `598` Controllers) of the new address assignment via the _**Define List of Targets (DEFTGTS)**_ CCC (I3C `599` Specification _**Section 5.1.9.3.7**_ ). 

- `600` As emphasized in the I3C Specification, the thing that distinguishes a Device participating on the Bus as an `601` I3C Device from a Device that remains in its initial power-on state is whether it has an I3C Dynamic `602` Address. This distinction is particularly important when the I3C-capable Device is also capable of acting as `603` an I[2] C Device on a Legacy I[2] C Bus. Such Devices will have their 50 ns Spike Filters enabled and active on `604` initial power-on, until they know they are on an I3C Bus. This Spike Filter must be taken into account by `605` the Host layer (i.e., the higher layer that controls the Primary Controller, and through it the I3C Bus) in `606` performing Bus Initialization and initiation of the Dynamic Address Assignment procedure (via the `607` ENTDAA, SETDASA, or SETAASA CCC). Devices that power-up with the Spike Filter in effect won’t `608` know that they’re on an I3C Bus (as opposed to a Legacy I[2] C bus) until they receive an I3C Dynamic `609` Address. 

`610` The Host layer and Controller must also take into consideration the fact that the I[2] C-compatible Devices `611` will re-enable their 50 ns Spike Filters after the RSTDAA CCC is sent. This means that the Active `612` Controller must send a valid I3C Address Header with the 7’h7E Broadcast Address at a speed sufficiently `613` slow to be received even with the Spike Filter enabled. Only then will such Devices recognize that they are `614` on an I3C Bus, and as a result disable their Spike Filters (see _**Section 5.1.2.1.1**_ of the I3C Specification `615` _**[MIPI06]**_ ). 

- `616` _**Note:**_ 

`617` _I3C Target Devices that use the standard Hot-Join method (see_ _**Section 5.1.5** of the I3C_ `618` _Specification_ _**[MIPI06]** ) will not have the 50 ns Spike Filter, because the I[2] C specification does not_ `619` _support Hot-Join functionality, and such Target Devices would assume by default that they are on_ `620` _an I3C Bus._ 

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

23 

App Note for I3C: General Topics 

App Note Version 1.1 27-Apr-2022 

## `621` **5.4 Use of Legacy I[2] C Devices** 

- `622` By design, the I3C protocol can operate on an I3C Bus where Legacy I[2] C Devices are also connected. `623` However, not all Legacy I[2] C Targets are fully supported. When using Legacy I[2] C Devices on an I3C Bus, `624` System Designers must ensure that compatibility requirements are satisfied, and that the legacy devices do `625` not significantly degrade I3C Bus performance. 

- `626` The primary consideration in this regard is that most Legacy I[2] C Devices found in the market are designed 

- `627` to ignore SCL High pulses that are shorter than 50 ns. This feature is known as the Spike Filter. The `628` presence of the Spike Filter allows many I3C Bus transactions to execute at higher speed. 

- `629` _**Note:**_ 

- `630` 

   - _In version 7.0 of the I[2] C Specification_ _**[NXP01]** , the SCL high pulse tHIGH must be greater than_ 

- `631` _260 ns for Fast-mode+, greater than 60 ns for High-speed with 100 pF Bus load, or greater than_ `632` _50 ns for Ultra Fast-mode._ 

- `633` The I3C Specification defines several categories of Legacy I[2] C Devices and characterizes how an I3C Bus `634` will perform if they are present (see _**Table 4 Legacy I[2] C-Only Target Categories and Characteristics**_ in `635` _**Section 5.1.1.1**_ , and _**Table 7 Legacy I[2] C Virtual Register (LVR)**_ in _**Section 5.1.1.2.3 [MIPI06]**_ ). 

## `636` **5.4.1 Considerations for Legacy I[2] C Devices** 

- `637` The I3C Specification classifies Legacy I[2] C Devices into three categories based on how they affect I3C Bus `638` performance: 

- `639` • **Index 0 Devices** have a Spike Filter that will cause them to ignore any SCL High pulse shorter `640` than 50 ns. 

- `641` If Index 0 I[2] C Devices are present on the Bus, then the Active Controller can still communicate `642` with I3C Devices on the Bus at up to the maximum SCL clock frequency (fSCL), as long as the `643` SCL High pulses for such transfers are shorter than 50 ns. 

- `644` • **Index 1 Devices** will not have a Spike Filter _per se_ but are tolerant of the maximum SCL clock `645` frequency. 

- `646` If Index 1 I[2] C Devices are present on the Bus, then they will ignore any transfers to I3C Devices. `647` The Active Controller can still communicate with I3C Devices on the Bus using up to the `648` maximum SCL clock frequency (fSCL), as long as the SCL High pulses for such transfers are `649` shorter than 50 ns. 

- `650` • **Index 2 Devices** will not have a Spike Filter _per se_ and they are not tolerant of the maximum SCL `651` clock frequency. 

- `652` Index 2 devices will significantly downgrade the Bus performance: If Index 2 I[2] C Devices are `653` present on the Bus, then the Active Controller must restrict all transfer rates to the maximum SCL `654` clock frequency that the Index 2 I[2] C Devices support. This limits the performance of the I3C Bus `655` and can also prevent some HDR Mode transfers with minimum clock requirements. 

- `656` For optimal performance of the I3C Bus, the System Designer should entirely avoid the use of Index 2 `657` Devices. If the use of Index 2 devices cannot be avoided, then they should be separated from the I3C `658` Devices by placing the Index 2 devices on a downstream Bus segment (i.e., using a Bridge Device) where `659` they will not be able to impact transfer rates on the I3C Bus segment. 

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

24 

App Note Version 1.1 27-Apr-2022 

App Note for I3C: General Topics 

## `660` **5.4.1.1 Detecting the Presence of the 50 ns Spike Filter** 

`661` This section describes a possible method for detecting whether a given I[2] C Device has a 50 ns Spike Filter, `662` or will properly tolerate (i.e., will ignore) higher-speed I3C transfers. (Other methods are also possible). 

`663` The test is done by sending a private read/write communication after sending the I3C Broadcast Address `664` (see _**Figure 5**_ ). The signaling marked in grey is handled as Open Drain transfers at an I[2] C-compliant SCL `665` frequency, and the signaling marked in blue is handled as a higher-speed transfer where either the SCL `666` High width (i.e., parameter tDIG_High) is less than 50 ns, or I3C Mixed Bus timing is maintained. 

|**START**|**7-bit Broadcast Address**|**RnW=0**|**ACK from DUT**||
|---|---|---|---|---|
|Repeated START|7-bit I2C Address|RnW=0|NACK from DUT|STOP|



```
667
```

## **Figure 5 Spike Filter Detection Pattern** 

`668` From the Legacy I[2] C Device’s response to its I[2] C Static Address after the Repeated START, the Controller `669` will know whether the device is capable of properly tolerating (i.e., ignoring) higher-speed transfers: 

- `670` • **ACK:** A device that responds with ACK is not capable of ignoring higher-speed transfers, either `671` because it has no 50 ns Spike Filter, or for some other reason: it successfully detected and `672` processed the high-speed Bus transfer. Such a device would likely be Index 2. 

- `673` • **NACK:** If the Controller receives NACK, then the device properly ignored the higher-speed `674` transfer, either because it possesses a 50 ns Spike Filter (making it an Index 0 device), or for some `675` other reason (making it an Index 1 device): it failed to detect and process the higher-speed Bus `676` transfer. 

```
676
```

`677` _**Note:**_ 

`678` _Legacy I[2] C Devices will not respond to the I3C Broadcast Address (7’h7E / W), and the Bus might_ `679` _have a combination of Legacy I[2] C Devices and I3C Devices._ 

`680` This also applies to I[2] C/I3C capable Devices which are supposed to respond to I[2] C commands directed to `681` them using their I[2] C Static Address. If no Dynamic Address is assigned to these Devices and they don’t `682` know that they are on an I3C Bus (per _**Section 5.1.2.2.2**_ of the I3C Specification _**[MIPI06]**_ ), then their `683` 50 ns Spike Filters will be engaged and they will behave as Legacy I[2] C Devices in all other respects. `684` However, if such Devices detect a START followed by the I3C Broadcast Address (i.e., with their Spike `685` Filter initially enabled), then such Devices will disable their Spike Filters and act as I3C Devices. 

- `686` 

## _**Note:**_ 

`687` _A previous version of this Application Note indicated that such I[2] C/I3C capable Devices could_ `688` _determine whether to act as I3C Devices based on whether they had been assigned a Dynamic_ `689` _Address. However, more recent versions of the I3C and I3C Basic Specifications_ _**[MIPI06]** have_ `690` _clarified the requirements. Per_ _**Section 5.1.2.2.2** , the Controller is now required to transmit an SDR_ `691` _Frame with START followed by the I3C Broadcast Address (7’h7E / W) at slower speeds, in order to_ `692` _allow such I[2] C/I3C capable Devices to detect that they are actually on an I3C Bus, disengage their_ `693` _Spike Filters, and act as I3C Devices. As a result, the test procedure above would need to be_ `694` _applied_ _**before** the Controller transmits the required START followed by Broadcast Address at_ `695` _slower speeds, so that such Devices can disengage their Spike Filters after the test procedure._ `696` _Alternatively, the test procedure might not be necessary._ 

25 

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

App Note for I3C: General Topics 

App Note Version 1.1 27-Apr-2022 

## `697` **5.4.2 I[2] C Clock Stretch is Not Allowed in I3C** 

- `698` In I[2] C the Controller drives the SCL line in Open Drain. This creates the possibility for I[2] C Target Devices 

- `699` to delay the I[2] C Bus when desired, by holding the SCL line Low. Delaying the I[2] C bus in this way is called `700` “clock stretching”. 

- `701` In I3C, by contrast, the Active Controller generally drives the SCL line in Push-Pull. This brings several `702` advantages and allows the I3C Bus to be optimized Bus for speed, efficiency, and loading. However, it also `703` means that I3C Target Devices are not permitted to hold the SCL line Low. As a result, I[2] C-style clock `704` stretching is not allowed in I3C. 

## `705` **5.4.3 Legacy Virtual Register (LVR) Use** 

- `706` Every Legacy I[2] C Device that can be connected to the I3C Bus has an associated read-only Legacy Virtual `707` Register (LVR) describing the device’s significant features. Since these are Legacy I[2] C Devices, it is `708` understood that this I3C-specific register will not actually exist on the device as hardware. Instead, the LVR `709` is expected to exist virtually, for example as part of the software driver for the device. When a Legacy I[2] `710` Device is present on an I3C Bus, fields in its LVR indicate what I[2] C Modes the device supports, and its `711` maximum SCL clock frequency. The LVR fields are defined in the I3C Specification in _**Table 5 Bus**_ `712` _**Characteristics Register**_ at _**Section 5.1.1.2.3 [MIPI06]**_ . 

- `713` In particular, LVR Bits[7:5] define the device’s Index value, which indicates whether such the device has a `714` Spike Filter (can otherwise tolerate Bus transfers at up to the maximum I3C clock speed). The Host that `715` directs the Primary Controller must have this knowledge before any Controller-capable Device attempts to `716` drive I3C transfers. The reason is that if any Legacy I[2] C Devices have no Spike Filter (or for any other `717` reason cannot tolerate Bus transfers at the maximum I3C clock speed), then the performance of all I3C `718` transfers on the Bus will be impacted, and the Controller(s) will need to limit the use of SDR transfers at `719` maximum clock speed. Additionally, such constraints might limit which HDR Modes and clock speeds can `720` be used. 

- `720` 

`721` LVRs are typically transferred to the Primary Controller of the I3C Bus before the Bus is configured. As a `722` result, the Primary Controller knows the content of the LVR for every I[2] C Device at Bus configuration, and `723` this information can be transferred to any Secondary Controller(s) present on the I3C Bus by using the `724` _**Define List of Targets (DEFTGTS)**_ CCC (see _**Section 5.1.9.3.7**_ in the I3C Specification _**[MIPI06]**_ ). 

26 

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

App Note Version 1.1 27-Apr-2022 

App Note for I3C: General Topics 

## `725` **5.5 I/O Characteristics** 

## `726` **5.5.1 Pad Capacitance** 

- `727` As previously stated, the pad capacitance adds to the whole Bus capacitance and needs to be considered `728` when computing the effective Bus frequency or other Bus parameters. The pad capacitance of a Device also `729` contributes directly to the skew of the signals that the Device drives on the Bus, the Device internal delay, `730` and the tSCO. For this reason, it is important that Device vendors accurately specify the maximum pad `731` capacitance such that System Designers can optimize I3C Bus performance for the total capacitance seen `732` on the SDA and SCL lines. 

## `733` **5.5.2 SDA Drive Strength** 

- `734` As previously discussed, the pad drive strength is another factor that contributes to the signal skew and to a `735` Device’s ability to drive the pad within the required rise and fall time. Notably, I[2] C (Fm/Fm+) and I3C can `736` have different specified drive strengths, thus care should be taken to minimize any impact upon Bus `737` performance due to reflections, overshoot, etc. 

- `738` Most Bus timing parameters in the I3C Specification were developed using a 90 Ω output drive impedance `739` as the measurement reference, and under those conditions the minimum recommended Bus drive strength is `740` 4 mA. 

- `740` 

- `741` Greater drive strength can be implemented, as long as the Bus reflections and system power requirements `742` are not affected, and care is taken to avoid overshoot. 

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

27 

App Note for I3C: General Topics 

App Note Version 1.1 27-Apr-2022 

## `743` **5.6 Bus Topologies** 

- `744` **5.6.1 Bus Topology Types** 

## `745` **5.6.1.1 Basic Bus Topologies** 

`746` For purposes of illustration, this section of the Application Note defines and discusses three Bus topologies: `747` Multi-Drop, Point-to-Point, and Star-on-Stick. If needed for a particular system design or use case, a given `748` I3C Bus might use more than one of these Bus topologies together (see _**Section 5.6.1.2**_ ). When calculating `749` the distance between a Controller and its Target(s), a System Designer should consider all three Bus `750` topologies. 

- `751` • **Multi-Drop Bus Topology** ( _**Figure 6**_ ). A single Controller is connected to two or more Targets A `752` and B (etc.), all attached on the same branch. 

- `753` The distance of the medium between the Controller and Target A is **L1** , and the distance from `754` Target A to Target B is **L2** ; thus, Target B’s distance **LT** from the Controller is **L1 + L2** . 

- `755` _**Figure 6**_ also shows each Target connected through a stub with length **St** , and after the stub `756` another medium of length **L3** . As a result, target A’s distance from the Controller is **L1 + St + L3** , `757` and Target B’s distance from the Controller is **L1 + L2 + St + L3** . Stub length plays an important `758` role in signal integrity of the I3C Bus signals (SDA and SCL). 

- `759` 

The medium could be board trace only, or board and cables. 

```
760
```

```
761
```

**==> picture [260 x 193] intentionally omitted <==**

**----- Start of picture text -----**<br>
I3C<br>CONTROLLER<br>ACTIVE<br>St Stub Stub<br>I3C I3C<br>TARGET A TARGET B<br>LEGEND<br>I3C CONTROLLER<br>I3C TARGET<br>(i.e., Primary)<br>**----- End of picture text -----**<br>


**Figure 6 Multi-Drop Bus Topology** 

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

28 

App Note Version 1.1 27-Apr-2022 

App Note for I3C: General Topics 

- `762` • **Point-to-Point Bus Topology** ( _**Figure 7**_ ) has one Controller connected to one Target. 

- `763` For this topology, the two Devices are connected by a board trace of Length **LT** . 

- `764` The medium could be board and cable, board trace only, or any other medium. 

```
765
```

```
766
```

**==> picture [231 x 108] intentionally omitted <==**

**----- Start of picture text -----**<br>
I3C I3C<br>CONTROLLER TARGET<br>ACTIVE<br>LEGEND<br>I3C CONTROLLER<br>I3C TARGET<br>(i.e., Primary)<br>**----- End of picture text -----**<br>


**Figure 7 Point-to-Point Bus Topology** 

- `767` • **Star-on-Stick Bus Topologies** ( _**Figure 8**_ ) are for Multi-drop Busses where all of the Targets are `768` far apart from the Controller, but also close to each other (i.e., **L1** is much greater than **L2** ). 

- `769` For this topology, the distance from the Controller to each Target is **L1 + St + L2** , and **L1** is much `770` greater than **L2** . 

- `771` Although _**Figure 8**_ shows equal distances for each of the Target Devices, in practice there could be `772` per-Target distance variations. The System Designer must make sure that the distance for each `773` Target is as equal as possible. In Star-on-Stick topologies, stubs also play an important role in I3C `774` Bus signal integrity (SDA and SCL). 

```
775
776
```

**==> picture [348 x 236] intentionally omitted <==**

**----- Start of picture text -----**<br>
I3C<br>TARGET A<br>Stub<br>I3C Stub I3C<br>CONTROLLER TARGET C<br>ACTIVE<br>St Stub<br>I3C<br>LEGEND TARGET B<br>I3C CONTROLLER<br>I3C TARGET<br>(i.e., Primary)<br>**----- End of picture text -----**<br>


**Figure 8 Star-on-Stick Bus Topology** 

Copyright © 2018–2022 MIPI Alliance, Inc. 

29 

**Public Release Edition** 

App Note for I3C: General Topics 

App Note Version 1.1 27-Apr-2022 

## `777` **5.6.1.2 Complex Bus Topologies** 

- `778` By combining the principles of these three basic Bus topologies, a System Designer could extend an I3C `779` Bus to construct more complex Bus topologies, and optionally include more advanced I3C Devices. _**Figure**_ `780` _**9**_ shows an example I3C Bus that includes a simple I3C Target Device, a composite I3C Device that `781` contains multiple I3C Targets (i.e., as multiple dies or wafers with internal traces or wires), and a more `782` advanced I3C Device that presents multiple Virtual Targets using Shared Peripheral logic. (For more on `783` Virtual Targets, see the separate _**MIPI Alliance Application Note for Virtual Devices and Virtual Targets**_ `784` _**[MIPI08]**_ ). 

- `785` • In this example, the per-Device distance from the Controller to each physical Device could be the `786` same (i.e., based on the ideal Star-on-Stick Bus topology), whereas the length of the internal traces `787` or wires inside the composite Device might vary. This will depend on the per-Target distance from `788` the Device’s external pins to the I3C Target’s pads. In such a configuration, the theoretical distance `789` from the Controller to each integrated Target would vary, but would be at least **L1 + St + L4** plus `790` the actual per-Target trace or wire distance inside the integrated Device. If these per-Target `791` trace/wire distances differ for each integrated Target, then the Bus topology becomes more `792` complex. 

- `793` • Alternately (although this is not a recommended configuration), the multi-Target integrated Device `794` might present separate external I3C pins for each I3C Target. 

- `795` • By contrast, an advanced I3C Device that uses Shared Peripheral logic to present multiple Virtual `796` Targets has a simpler Target distance calculation (e.g., **L1 + St + L3** ) since the Virtual Targets are `797` not part of this calculation. For such a Device the Shared Peripheral logic would handle the I3C `798` transfers, so the factor to consider would be the internal trace or wire distance between the pins `799` and the Shared Peripheral’s I/O pads. Device manufacturers should ensure that the I/O pads and `800` Shared Peripheral logic are as close to the pins as possible. 

- `801` • In all of the above cases, I3C Device manufacturers that make either multi-Target integrated `802` Devices or composite Devices should publish the Device’s internal trace or wire lengths, so that `803` System Designers can have adequate information to calculate the per-Target length and understand `804` the actual Bus topology. 

```
805
806
```

**==> picture [373 x 248] intentionally omitted <==**

**----- Start of picture text -----**<br>
I3C<br>TARGET<br>(Simple)<br>Stub SHARED PERIPHERAL<br>I3C<br>CONTROLLER I3C I3C<br>Stub VIRTUAL VIRTUAL<br>TARGET TARGET<br>ACTIVE<br>Stub<br>I3C DEVICE (Integrated Package)<br>Internal traces or wires not shown<br>LEGEND<br>I3C CONTROLLER I3C I3C<br>(i.e., Primary) I3C TARGET TARGET TARGET<br>I3C DEVICE I3C DEVICE<br>(Integrated) (Virtualized)<br>**----- End of picture text -----**<br>


**Figure 9 Complex Bus Topology** 

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

30 

App Note Version 1.1 27-Apr-2022 

App Note for I3C: General Topics 

## `807` **5.6.2 Trace/Medium** 

`808` In the basic Bus topologies shown in _**Figure 6**_ through _**Figure 8**_ , the medium connected to the Devices `809` could be FR4 board trace, or board trace + cable, or trace + via + trace + cable, etc. The System Designer `810` must make sure that the length of the trace or medium is chosen to meet the maximum Bus capacitance `811` supported by the I3C Specification. 

`812` **Example:** A Point-to-Point Bus topology targeting 20 inches will result in 44 pF of board trace capacitance, `813` where FR4 is 2.2 pF / inch. 

- `814` 

## _**Note:**_ 

`815` _The case of FR4 trace + Cable will result in different medium capacitance, and the calculation will_ `816` _not be direct as compared to single FR4 trace, because the discontinuity in the signal board trace_ `817` _also impacts the capacitance._ 

## `818` **5.6.2.1 Length** 

- `819` The length of board trace that can be supported depends upon various factors, key among them being: 

- `820` • **Bus Topologies:** Bus topologies impact the length supported for SDR/DDR mode and for HDR `821` mode. Point-to-Point topologies will permit longer board traces or medium, assuming fixed `822` capacitance from load. 

- `823` • **Device Capacitance:** Device capacitance impacts Bus performance and maximum length for the `824` targeted medium. The number of Devices present on the Bus will also increase the Bus `825` capacitance, thus reducing medium length. 

- `826` • **Reflections:** Signal integrity will affect the targeted medium length. The System Designer must be `827` sure to avoid reflection or discontinuity, which will directly reduce targeted Bus length. 

```
828
```

- **Medium:** Selection of a lossy medium will reduce targeted board trace length. 

## `829` **5.6.2.2 Material** 

`830` The I3C Specification _**[MIPI06]**_ does not define the physical conducting medium material: it can be PCB `831` traces, cables, and/or connectors. However, the characteristics of the selected material(s) (such as capacitive `832` impedance, resistive loss, and physical dimensions) will directly impact the overall maximum length that `833` can be achieved. The System Designer must verify that the signal degradation for the selected medium `834` configuration will meet the constraints set by the electrical and timing specifications given in _**Section 6**_ of `835` the I3C Specification _**[MIPI06]**_ . 

## `836` **5.6.2.3 Design/Matching** 

`837` The SDA and SCL lines should be matched, both in terms of silicon design and in terms of board design. A `838` mismatch will result in skew, and will limit the timing budget. This is also true for the more complex case `839` of Multi-Lane SDA configurations. 

`840` An impedance mismatch between the board and the I/O buffer will result in reflections, directly impacting `841` and reducing the timing window for read/write operations. 

`842` For writes, skew is a key parameter that must be controlled for SDR Mode, as well as some HDR Modes. `843` Some HDR Modes perform transfers where the SCL and SDA lines are both being driven. In such cases, `844` Read/Write skew will limit the timing window. This applies to all HDR-TSP/TSL Read transfers, and `845` optionally to HDR-BT Read transfers (i.e., when the Target drives SCL) if allowed by the Controller. 

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

31 

App Note for I3C: General Topics 

App Note Version 1.1 27-Apr-2022 

## `846` **5.6.2.4 GND Management** 

- `847` Although this is not stated in the I3C Specification, in order to ensure good noise immunity performance `848` for reliable operation of single-ended interfaces it is recommended to hold Ground bounce between `849` Controller and Target to below ±50 mV. Given the limited current of the output Driver, the source of this `850` voltage bounce is expected to be parasitic inductances (which can and should be minimized through the use `851` of good PCB layout practices). 

## `852` **5.6.2.5 Stubs** 

- `853` Stubs play a role in maintaining signal integrity. Improperly terminated stubs will result in discontinuity, `854` which in turn will produce reflection and timing loss. The longer the stub, the greater the reflection. The `855` maximum recommended stub delay is 250 ps, which typically corresponds to 1.5" on a FR4 line. 

## `856` **5.6.3 Mixed Bus Considerations** 

`857` I3C supports Legacy I[2] C Devices using Fast-mode (400 KHz) and FastMode+ (1 MHz) with the 50 ns `858` Spike Filter, but no other I[2] C modes, nor Legacy I[2] C Devices that stretch the clock. 

`859` Additionally, if any Legacy I[2] C Devices with Index 2 (i.e., that are unable to tolerate higher-speed transfers `860` and do not have the 50 ns Spike Filter) are present on the Bus, then it is a Mixed Slow/Limited Bus (per `861` I3C Specification _**Section 5.1.2.4 [MIPI06]**_ ), so the Controller will be unable to utilize the I3C Bus for `862` higher-speed transfers. Additionally, because the Index 2 I[2] C Devices would not properly ignore HDR `863` Mode transfers, the HDR Modes will also be unavailable. 

## `864` **5.6.4 Hot-Join Capability** 

- `865` The I3C Bus protocol supports a Hot-Join mechanism which allows Target Devices to join the I3C Bus `866` after it has already been configured. To ensure stability when a Target Device joins the I3C Bus, the I3C `867` Specification _**[MIPI06]**_ defines the conditions under which a Target Device can issue a Hot-Join Request: `868` the Target must first know (or be informed) that the Bus is an I3C Bus, and is then required to wait for a `869` Bus Idle condition. 

- `870` 

## _**Note:**_ 

- `871` _For extensive detail regarding the Hot-Join feature, Hot-Plug, and related topics, see the separate_ `872` _**MIPI Alliance I3C Application Note: Hot-Join [MIPI09]** which expands on the Hot-Join section_ `873` _that appeared in earlier versions of this Application Note._ 

`874` If the System Designer plans to support Hot-Joining Devices (which might also be Hot-Plug Devices), then `875` to protect the Bus, care must be taken to ensure that I/O pads are safe when unpowered, and that any stub `876` lengths are factored into the overall topology (both before and after the Hot-Joining Devices are connected, `877` powered, and ready to act as I3C Targets). 

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

32 

App Note Version 1.1 27-Apr-2022 

App Note for I3C: General Topics 

## `878` **5.7 Physical/Electrical/Testing Considerations (I3C CTS)** 

- `879` In order to improve interoperability of products implementing the I3C interface, the MIPI Alliance I3C `880` Working Group has developed a Conformance Test Suite (CTS) for I3C and I3C Basic _**[MIPI10]**_ . 

- `881` This CTS contains tests designed to determine whether a product conforms to a subset of the requirements `882` defined in the latest versions of either the I3C Specification _**[MIPI03]**_ or the I3C Basic Specification `883` _**[MIPI05]**_ . 

- `884` In order to promote interoperability testing for I3C Devices in the marketplace, this version of the CTS `885` provides a thorough set of tests that focus on I3C’s essential capabilities: 

- `886` • SDR-only Devices without optional I3C capabilities 

- `887` • All Error Detection and Recovery methods (for both Controller Devices and Target Devices) 

- `888` • Basic HDR Enter/tolerance/Restart/Exit 

- `889` The I3C WG plans to continue expanding the scope of the CTS through future revisions, eventually `890` encompassing all required and optional features of the I3C Specification. 

- `891` The CTS is organized as one section of tests for a Controller device under test (DUT), and a separate `892` section of tests for a Target DUT. Within each section, the tests are correlated with the I3C Specification `893` Sections containing the related requirement(s), to make it easier to find the relevant Specification details. 

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

33 

App Note for I3C: General Topics 

App Note Version 1.1 27-Apr-2022 

## `894` **5.8 Bus High-Keeper** 

`895` The I3C Bus always needs a weak High-Keeper Pull-Up on the SDA line, for times when there is no active `896` drive and no strong Pull-Up resistor (or equivalent). The High-Keeper Pull-Up requirements are defined at `897` _**Section 5.1.3.1**_ of the I3C Specification _**[MIPI06]**_ . 

- `898` Per the I3C Specification, this High-Keeper Pull-Up can be provided in either of two ways: 

- `899` 1. The I3C Controller can be responsible for this, providing the Bus High-Keeper in some `900` appropriate manner. 

```
901
```

## _**Note:**_ 

`902` _If the Bus has multiple Controller-capable Devices (i.e., if there are any Secondary_ `903` _Controllers), then each one will also need to be able to provide the High-Keeper while it is the_ `904` _Active Controller. If any Secondary Controller cannot provide a High-Keeper while holding the_ `905` _Controller Role, then the second method below would need to be used. However, a Secondary_ `906` _Controller should disengage its High-Keeper whenever it is not the Active Controller (and_ `907` _especially after it has passed the Controller Role to another Controller-capable Device)._ 

- `908` 2. When not supported by the Active Controller (or not supported by all Controller-capable Devices), `909` the Bus must be wired with one or more weak passive Pull-Up resistors on the SDA line. These `910` could be 50 KΩ, 100 KΩ, or higher-value resistors. The exact value, and whether more than one `911` resistor is used in parallel, depends on the particular system design, in terms of leakage sources `912` (e.g., the number of Target Devices and Controller Devices over the Bus topology) and the `913` system’s noise induction characteristics. 

- `914` _**Note:**_ 

`915` _If the Active Controller will not be using its strong (i.e., Open Drain class) Pull-Up on the SDA_ `916` _line during the Bus Free condition or any other longer condition (i.e., the Bus Available_ `917` _condition or the Bus Idle condition), then a stronger passive Pull-Up resistor should be used._ `918` _This will prevent noise from causing false START requests._ 

- `919` Additionally, HDR-BT Mode uses a “Park1,High-Z” convention for certain protocol elements (such as `920` Transition Bytes, per the I3C Specification at _**Section 5.2.4.2 [MIPI06]**_ ) that require the SDA line to briefly `921` be in a High-Z state. This might require the Controller to momentarily disengage its High-Keeper (if it is `922` capable of doing so), otherwise the System Designer will have to select a sufficiently weak High-Keeper `923` Pull-Up (if wired), so long as the leakage and noise induction concerns listed above are addressed. 

`924` Under certain scenarios, the SCL line might also need a weak High-Keeper Pull-Up. If the Active `925` Controller will not be engaging a sufficiently strong Pull-Up on SCL when the Bus is in the Bus Free `926` condition (or other similar conditions where SCL is held High) or when the Active Controller is in deep- `927` sleep state, then a passive weak Pull-Up should be provided on the SCL line. Likewise, if HDR-TSP Mode `928` or HDR-TSL Mode will be used and the Active Controller will not be providing a weak High-Keeper Pull- `929` Up on SCL during the handoff procedure (i.e., Bus Turnaround to a Target for a Read), then a weak passive `930` Pull-Up must be wired onto SCL. 

- `931` _**Note:**_ 

`932` _For the High-Keeper Pull-Up on the SCL line, the exact value, and whether more than one resistor_ `933` _is used in parallel, depends on the particular system design. While the considerations will be similar_ `934` _to those used for the SDA line, leakage sources on the Bus will likely be far less than for the SDA_ `935` _line, since the SCL line is passive for most Target Devices, and the incidence of noise on the SCL_ `936` _line is less likely. It is important that this passive High-Keeper Pull-Up is strong enough to hold SCL_ `937` _High during a long-idled Bus state._ 

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

34 

App Note Version 1.1 27-Apr-2022 

App Note for I3C: General Topics 

`938` **Example:** If the total leakage current is determined to be 10 µA from the I3C Devices on the SDA, `939` and we are using a 3.3V Bus, then the minimum resistance needed is: 

`940` 3.3 V / 0.00001 A = 330 KΩ. 

`941` In this example, the System Designer must allow for noise current, which will be lowered by the `942` capacitance of the line; for example, a value of 20 µA displacement can be assumed due to the `943` calculated capacitance of the line flattening a spike of ~2 V ground coupled. The System Designer `944` can simply sum those to equivalent leakages (since it is not typically a concern when noise is in `945` the opposite direction of static leakage, it is only a concern when it is in the same direction)to `946` reach a sum of 110 KΩ. In this example, it is typically safe  to use a 100 KΩ Pull-Up resistor. 

- `947` Further, for a long trace line the System Designer should typically place more than one resistor in parallel `948` along the trace, to ensure stability regardless of the source and placement of the leakage or noise. 

- `949` _**Note:**_ 

`950` _This resistor’s only job is to keep the V above VIH (and, in most cases, the difference of VIH − Vhys)_ `951` _after it is already parked at High (i.e., when it was previously driven High). As a result, a weaker_ `952` _High-Keeper Pull-Up could be used in cases of more noise, as long as the V remains above VIH._ `953` _The essential goal is to keep V above VIH_ _**for the I3C Devices on the Bus** , since a V dip along an_ `954` _empty stretch of trace would only matter if it were to impact I3C Devices in other areas._ 

## `955` **5.9 Bridge Devices** 

- `956` The MIPI I3C Specification _**[MIPI06]**_ covers inter-Bus bridging support, both passively and actively. In all `957` cases, the bridged endpoints (i.e., the Devices that are being bridged to the I3C Bus) are presented as I3C `958` Virtual Targets, each with its own I3C Dynamic Address, which transact with the I3C Bus through the `959` Bridge Device. 

- `960` _**Note:**_ 

`961` _For extensive detail regarding Bridge Devices, Virtual Targets, and related topics, see the separate_ `962` _**MIPI Alliance I3C Application Note: Virtual Devices and Virtual Targets [MIPI08]** which_ `963` _expands on the Bridge Devices section that appeared in earlier versions of this Application Note._ 

35 

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

App Note for I3C: General Topics 

App Note Version 1.1 27-Apr-2022 

This page intentionally left blank. 

36 

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

