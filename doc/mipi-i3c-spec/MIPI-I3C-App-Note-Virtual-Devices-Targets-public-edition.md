## **I3C Application Note: Virtual Devices and Virtual Targets** 

**For MIPI I3C[®] v1.2 and I3C Basic[TM] v1.2** 

**App Note Version 1.2 29 August 2025** 

MIPI Board Approved 31 November 2025 **Public Release Edition** 

This is an informative document, not a MIPI Specification. 

Various rights and obligations that apply solely to MIPI Specifications (as defined in the MIPI Membership Agreement and MIPI Bylaws) including, but not limited to, patent license rights and obligations, do not apply to this document. 

This document is subject to further editorial and technical development. 

Copyright © 2021–2025 MIPI Alliance, Inc. 

I3C Application Note: Virtual Devices and Virtual Targets 

App Note Version 1.2 29-Aug-2025 

## **NOTICE OF DISCLAIMER** 

The material contained herein is provided on an “AS IS” basis. To the maximum extent permitted by applicable law, this material is provided AS IS AND WITH ALL FAULTS, and the authors and developers of this material and MIPI Alliance Inc. (“MIPI”) hereby disclaim all other warranties and conditions, either express, implied or statutory, including, but not limited to, any (if any) implied warranties, duties or conditions of merchantability, of fitness for a particular purpose, of accuracy or completeness of responses, of results, of workmanlike effort, of lack of viruses, and of lack of negligence. ALSO, THERE IS NO WARRANTY OR CONDITION OF TITLE, QUIET ENJOYMENT, QUIET POSSESSION, CORRESPONDENCE TO DESCRIPTION OR NON-INFRINGEMENT WITH REGARD TO THIS MATERIAL. 

IN NO EVENT WILL ANY AUTHOR OR DEVELOPER OF THIS MATERIAL OR MIPI BE LIABLE TO ANY OTHER PARTY FOR THE COST OF PROCURING SUBSTITUTE GOODS OR SERVICES, LOST PROFITS, LOSS OF USE, LOSS OF DATA, OR ANY INCIDENTAL, CONSEQUENTIAL, DIRECT, INDIRECT, OR SPECIAL DAMAGES WHETHER UNDER CONTRACT, TORT, WARRANTY, OR OTHERWISE, ARISING IN ANY WAY OUT OF THIS OR ANY OTHER AGREEMENT RELATING TO THIS MATERIAL, WHETHER OR NOT SUCH PARTY HAD ADVANCE NOTICE OF THE POSSIBILITY OF SUCH DAMAGES. 

The material contained herein is not a license, either expressly or impliedly, to any IPR owned or controlled by any of the authors or developers of this material or MIPI. Any license to use this material is granted separately from this document. This material is protected by copyright laws, and may not be reproduced, republished, distributed, transmitted, displayed, broadcast or otherwise exploited in any manner without the express prior written permission of MIPI Alliance. MIPI, MIPI Alliance and the dotted rainbow arch and all related trademarks, service marks, tradenames, and other intellectual property are the exclusive property of MIPI Alliance Inc. and cannot be used without its express prior written permission. The use or implementation of this material may involve or require the use of intellectual property rights (“IPR”) including (but not limited to) patents, patent applications, or copyrights owned by one or more parties, whether or not members of MIPI. MIPI does not make any search or investigation for IPR, nor does MIPI require or request the disclosure of any IPR or claims of IPR as respects the contents of this material or otherwise. 

Without limiting the generality of the disclaimers stated above, users of this material are further notified that MIPI: (a) does not evaluate, test or verify the accuracy, soundness or credibility of the contents of this material; (b) does not monitor or enforce compliance with the contents of this material; and (c) does not certify, test, or in any manner investigate products or services or any claims of compliance with MIPI specifications or related material. 

Questions pertaining to this material, or the terms or conditions of its provision, should be addressed to secretary@mipi.org. 

ii 

Copyright © 2021–2025 MIPI Alliance, Inc. **Public Release Edition** 

App Note Version 1.2 29-Aug-2025 

I3C Application Note: Virtual Devices and Virtual Targets 

## **Contents** 

|**Contents**|**Contents**|**Contents**|
|---|---|---|
|**Figures .................................................................................................................................v**|||
|**Tables ................................................................................................................................. vi**|||
|**Release History ................................................................................................................ vii**|||
|**1**|**Introduction .................................................................................................................1**||
||1.1|Scope ............................................................................................................................... 1|
|**2**|**Terminology .................................................................................................................2**||
||2.1|Definitions ....................................................................................................................... 2|
||2.2|Abbreviations ................................................................................................................... 3|
||2.3|Acronyms ......................................................................................................................... 3|
|**3**|**References ....................................................................................................................4**||
|**4**|**Overview ......................................................................................................................5**||
||4.1|Supported Capabilities ..................................................................................................... 5|
||4.2|Using Added Functionality .............................................................................................. 6|
|**5**|**Virtual Target Concepts ..............................................................................................7**||
||5.1|Simple Integrated I3C Devices ........................................................................................ 9|
||5.1.1|Internal Topologies ..................................................................................................... 10|
||5.1.2|Number of Virtual Targets in a Unit ........................................................................... 13|
||5.1.3|Virtual Target Power Management ............................................................................. 14|
||5.1.4|Bus Configuration Registers ....................................................................................... 14|
||5.1.5|Dynamic Address Assignment and Provisioned ID Management .............................. 15|
||5.2|Composite I3C Devices ................................................................................................. 17|
||5.2.1|Architectural Overview .............................................................................................. 17|
||5.2.2|Shared Peripheral Logic ............................................................................................. 18|
||5.2.3|Enabling Virtual Target Transactions.......................................................................... 24|
|**6**|**Connecting to Other Buses via I3C Virtual Targets...............................................26**||
||6.1|Common Concepts ......................................................................................................... 26|
||6.1.1|Manager Function ....................................................................................................... 27|
||6.1.2|Configuration of Downstream Virtual Targets ........................................................... 27|
||6.2|Bridge Devices............................................................................................................... 29|
||6.2.1|Architectural Overview .............................................................................................. 29|
||6.2.2|Bridge Manager Function ........................................................................................... 30|
||6.2.3|Initialization and Configuration.................................................................................. 31|
||6.2.4|Bridged Endpoints Exposed as Virtual Targets .......................................................... 35|
||6.2.5|Bridged Devices and IBI ............................................................................................ 35|
||6.3|Routing Devices............................................................................................................. 36|
||6.3.1|Architectural Overview .............................................................................................. 36|
||6.3.2|Routing Manager Function ......................................................................................... 37|
||6.3.3|Downstream Bus Target Presentation ......................................................................... 38|
||6.3.4|Support for Remote Downstream Buses .................................................................... 42|
||6.3.5|Support for Controller Role or Segment Secondary Controller ................................. 44|



Copyright © 2021–2025 MIPI Alliance, Inc. **Public Release Edition** 

I3C Application Note: Virtual Devices and Virtual Targets 

App Note Version 1.2 29-Aug-2025 

|6.4|Hub Devices................................................................................................................... 46|
|---|---|
|6.4.1|Architectural Overview .............................................................................................. 47|
|6.4.2|Hub Manager Function ............................................................................................... 48|
|6.4.3|Isolation Logic and Transactions for Downstream Devices ....................................... 49|
|6.4.4|Support for Open Drain Pull-Up Handling ................................................................. 52|



iv 

Copyright © 2021–2025 MIPI Alliance, Inc. **Public Release Edition** 

App Note Version 1.2 29-Aug-2025 

I3C Application Note: Virtual Devices and Virtual Targets 

## **Figures** 

Figure 1 I3C Bus with I3C Devices and Virtual Targets .................................................................. 8 Figure 2 Integrated I3C Device with Targets as Hard IPs on a Die ................................................ 11 Figure 3 Integrated I3C Device with Targets as Stacked Dies or Wafers ....................................... 11 Figure 4 Integrated I3C Device with Targets Connected by Wire Interconnects ........................... 12 Figure 5 Integrated I3C Device with Targets Connected by Bridge or Interposer ......................... 12 Figure 6 Composite I3C Device with Virtual Targets and Shared Peripheral Logic ...................... 17 Figure 7 I3C Bridge Device with Virtual Targets and Bridged Endpoints ..................................... 29 Figure 8 I3C Routing Device with Downstream I3C Buses as Virtual Targets .............................. 36 Figure 9 I3C Routing Device with Mapped Downstream Targets ................................................. 41 Figure 10 I3C Routing Device with Remote Link to Downstream Bus ......................................... 42 Figure 11 I3C Routing Device with Downstream Secondary Controller Capability ..................... 44 Figure 12 I3C Hub Device with Isolation Logic and Downstream Target Devices ....................... 47 Figure 13 I3C Hub Device using External Pin for Open Drain Pull-Up ........................................ 52 

Copyright © 2021–2025 MIPI Alliance, Inc. **Public Release Edition** 

I3C Application Note: Virtual Devices and Virtual Targets 

App Note Version 1.2 29-Aug-2025 

## **Tables** 

Table 1 Section 5 Subjects ................................................................................................................ 7 Table 2 Comparison of I3C Device Integration Methods for Virtual Targets ................................ 13 Table 3 Application of RSTACT Defining Byte Values for Virtual Target Capable Devices ......... 21 

vi 

Copyright © 2021–2025 MIPI Alliance, Inc. **Public Release Edition** 

App Note Version 1.2 29-Aug-2025 

I3C Application Note: Virtual Devices and Virtual Targets 

## **Release History** 

||||
|---|---|---|
|**Date**|**Version**|**Description**|
|04-Sep-2021|v1.0|Initial Board approved release.|
|31-Dec-2025|v1.2|Board approved release.|



Copyright © 2021–2025 MIPI Alliance, Inc. **Public Release Edition** 

vii 

I3C Application Note: Virtual Devices and Virtual Targets 

App Note Version 1.2 29-Aug-2025 

This page intentionally left blank. 

viii 

Copyright © 2021–2025 MIPI Alliance, Inc. **Public Release Edition** 

App Note Version 1.2 29-Aug-2025 

I3C Application Note: Virtual Devices and Virtual Targets 

## `1` **1 Introduction** 

`2` The MIPI I3C Bus interface _**[MIPI03]**_ is an evolutionary specification that improves upon the legacy I²C `3` standard. It is designed to reduce the number of physical pins used in sensor system integration, and supports `4` low-power, high-speed digital communication typically associated with UART and SPI interfaces. `5` I3C’s main features include: 

- `6` 

- `7` 

   - In-Band Interrupts 

   - Dynamic Addressing 

- `8` • Multi-Controller and Multi-drop capabilities 

- `9` 

   - Hot-Join support 

- `10` • Backward compatibility with I²C 

`11` The I3C interface is expected to play a fundamental role in streamlining sensor integration in smartphones, `12` wearables, and Internet-of-Things (IoT) devices. The I3C interface is also extensible to newer and more `13` advanced used cases that go beyond the original scope of sensor integrations. This Application Note is `14` intended to help users understand how the I3C Bus can be extended to support device virtualization using `15` various types of composite I3C Devices, connections to other buses (including I3C Bus segments) and other `16` advanced integrations of I3C Target functionality. 

## `17` **1.1 Scope** 

- `18` This Application Note on Virtual Devices and Virtual Targets is intended to guide three different groups: 

- `19` • Those developing MIPI I3C Target Devices with advanced capabilities, to understand how these `20` Devices can expose advanced Virtual Device capabilities and implement them while remaining `21` compatible with MIPI I3C v1.2. 

- `22` • System Designers who have to design systems that integrate such advanced MIPI I3C Devices, `23` who need to know the implementation concerns with these advanced capabilities as well as the `24` configuration aspects that need to be considered by a MIPI I3C Controller and its connected Host `25` System. 

- `26` • MIPI I3C Controller software considerations in the one or more Controller-capable Devices in the `27` system. This includes users of both standardized Host Controller APIs and MCU/DSP firmware. 

- `28` This Application Note has several parts, each focusing on a different area and covering both required `29` considerations and optional ones, based on which advanced features are used in a given system. This approach `30` makes it easier for any of the targeted groups to focus on what matters to them based on what configurations `31` they will be working with. 

`32` This Application Note is also a complement to the _**I3C Application Note: General Topics [MIPI05]**_ , which `33` covers many fundamental topics of integrating MIPI I3C Devices in a system, as well as other I3C Bus `34` considerations that apply to all I3C Devices (i.e., electrical details and topology). 

`35` This Application Note is intended to be used together with the I3C Specification _**[MIPI03]**_ . Each Application `36` Note section corresponds to one or more Specification sections, primarily focusing on Specification `37` _**Section 4.3.11**_ , _**Electrical Specifications**_ . The Application Note amplifies the Specification with additional `38` context (e.g., analysis data to back up recommended use models) and details (e.g., specific usage notes for `39` more advanced use cases) that would not be appropriate in a protocol specification. 

Copyright © 2021–2025 MIPI Alliance, Inc. **Public Release Edition** 

I3C Application Note: Virtual Devices and Virtual Targets 

App Note Version 1.2 29-Aug-2025 

## `40` **2 Terminology** 

`41` See also _**Section 2.3**_ in the MIPI I3C Specification _**[MIPI03]**_ 

- `42` 

- `43` 

## **2.1 Definitions** 

**Active Controller:** The I3C Device that presently has control of the I3C Bus. 

`44` **Bridge Device:** As defined in the MIPI I3C Specification. A Device on the I3C Bus that allows conversion `45` from the native I3C Bus protocol to another protocol (such as SPI, UART etc.). 

- `46` **Controller:** An I3C Device (or Role embodied by such a Device) that is capable of controlling the I3C Bus. 

- `47` 

## _**Note:**_ 

- `48` _In previous versions of the I3C Specification, a Controller Device was called a “Master” Device. This_ `49` _Application Note uses the updated normative term “Controller.” Please note that the technical_ `50` _definition of such a Device, and its Role on an I3C Bus, are unchanged._ 

`51` **Downstream:** An I3C Bus or I3C Bus Segment that is subordinate to, or at a lower level of hierarchy `52` compared to, another I3C Bus (or Bus Segment). A Downstream Bus Segment typically receives I3C transfer `53` commands from its Upstream I3C Bus Controller (i.e., the Controller in charge of, or at a higher level of `54` hierarchy), and these I3C transfer commands are passed or translated via an agent Device (such as a Bridge `55` Device, Routing Device, or Hub Device) that spans both I3C Bus Segments. 

`56` **Hub Device:** An I3C Device that provides isolation between Upstream and Downstream I3C Bus Segments `57` having different electrical parameters, while still allowing transactions to pass between segments. 

- `57 58` **I3C Bus.** As defined in the MIPI I3C Specification. 

`59` **I3C Bus Segment:** An I3C Bus that exists within a hierarchy of several other I3C Buses, where a Bridge `60` Device, Routing Device, or Hub Device acts as an agent that relays transfer commands and responses from `61` one such I3C Bus to another Bus. 

`62` **Manager Function:** A Virtual Target presented by a Bridge Device, Routing Device or Hub Device that `63` allows the I3C Controller to manage and control the Device itself, via Private Write/Read transfers and/or `64` CCCs. 

- `65` **Master:** Deprecated term, see Controller. 

- `66` **Offline Capable:** As defined in the MIPI I3C Specification. 

- `67` **Route:** As defined in the MIPI I3C Specification. 

- `68` 

- `69` 

- `70` 

- `71` 

**Routing Device:** As defined in the MIPI I3C Specification. Device on the I3C Bus that allows conversations between two or more different I3C Buses (i.e., Bus Segments) through integrated logic on the given Device. The Routing Device (as distinct from a Bridge Device) buffers/queues the transactions using store-andforward architecture, causing the Device to be non-transparent. 

`72` **Routing Target Function:** A Virtual Target presented by a Routing Device which exposes a Route and `73` accepts Private Read or Private Write transactions to/from the Downstream I3C Bus Segment for that Route `74` through the Routing Device, as well as CCCs to control the parameters for that Route. See also “Route” in `75` the MIPI I3C Specification. 

`76` **Shared Peripheral:** Common logic of an I3C Device that handles low-level I3C Bus protocol, usually `77` including FIFOs or other buffers for Virtual Targets, and an interface to the rest of the system that enables `78` multiple applications, where each can present an individual Virtual Target. See “Peripheral” in the MIPI I3C `79` Specification. 

- `80` 

- `81` 

**Slave:** Deprecated term, see Target. 

**System Designer:** Engineer designing a system that includes an I3C Bus. 

Copyright © 2021–2025 MIPI Alliance, Inc. **Public Release Edition** 

2 

App Note Version 1.2 29-Aug-2025 

I3C Application Note: Virtual Devices and Virtual Targets 

- `82` **Target:** An I3C Device (or a Role embodied by such a Device) that can only respond to either Common or `83` individual commands from a Controller. Some Targets can initiate In-Band Interrupt requests on the I3C Bus. 

- `84` 

## _**Note:**_ 

- `85` _In previous versions of the I3C Specification, a Target Device was called a “Slave” Device. This_ `86` _Application Note uses the updated normative term “Target.” Please note that the technical definition_ `87` _of such a Device, and its Role on an I3C Bus, are unchanged._ 

- `88` **Target Reset:** The Target Reset mechanism allows the Controller to request a reset of specific Target Devices, `89` including: reset of the I3C Peripheral, reset of the whole Device, and wake from deepest sleep. Target Reset `90` uses a specialized pattern of Bus activity (specifically, an extension of the HDR Exit Pattern) that cannot `91` occur in any other way in the I3C protocol. 

- `92` **Upstream:** An I3C Bus or I3C Bus Segment that is in charge of, or at a higher level of hierarchy compared 

- `93` to, another I3C Bus (or Bus Segment). An Upstream Bus Segment has an I3C Bus Controller (i.e., Primary `94` Controller) that directs the operations on one or more subordinate Downstream Bus Segments, connected via 

- `95` an agent Device (such as a Bridge Device, Routing Device, or Hub Device) that spans both I3C Bus `96` Segments. 

- `97` **Virtual Function:** A virtualized entity or endpoint that exists within an I3C Device and which can receive 

- `98` I3C transfer commands that imply actions or special transactions that affect other I3C Devices, such as those 

- `99` on a Downstream I3C Bus Segment. Virtual functions are typically associated with Virtual Targets presented 

- `100` to the Upstream I3C Bus Segment, and often have associated functions that suit the purpose and capabilities `101` exposed by such an I3C Device _._ 

- `102` **Virtual Target:** As defined in the MIPI I3C Specification. May act as, or be presented as, a uniquely `103` addressable I3C Target on the I3C Bus. 

- `104` **Virtual Target Detect Operation:** A method for determining which Virtual Targets share the same Peripheral `105` logic within a particular I3C Device. 

## `106` **2.2 Abbreviations** 

- `107` e.g. For example (Latin: exempli gratia) `108` i.e. That is (Latin: id est) 

## `109` **2.3 Acronyms** 

- `110` BCR Bus Characteristics Register 

- `111` CCC Common Command Code 

- `112` DCR Device Characteristics Register 

- `113` I3C MIPI Improved Inter Integrated Circuit interface or its Specification document _**[MIPI03]**_ 

- `114` PID Provisional ID (i.e., 48-bit unique identifier for I3C Devices) 

- `115` SoC System-on-Chip 

- `116` VT Virtual Target 

Copyright © 2021–2025 MIPI Alliance, Inc. **Public Release Edition** 

I3C Application Note: Virtual Devices and Virtual Targets 

App Note Version 1.2 29-Aug-2025 

|`117`|**3**<br>**References**|**3**<br>**References**|
|---|---|---|
|`118`|[MIPI01]|_MIPI Alliance Specification for I3C® (Improved Inter Integrated Circuit)_,|
|`119`||version 1.2,|
|`120`||MIPI Alliance, Inc., 11 November 2024 (MIPI Board Adopted 11 February 2025).|
|`121`|[MIPI02]|_MIPI Alliance Specification for I3C BasicTM (Improved Inter Integrated Circuit)_,|
|`122`||version 1.2,|
|`123`||MIPI Alliance, Inc., 16 December 2024 (MIPI Board Adopted 17 April 2025).|
|`124`|[MIPI03]|Either**_[MIPI01]_**or**_[MIPI02]_**.|
|`125`|[MIPI04]|MIPI Alliance, Inc., “Current I3C Device Characteristic Register (DCR) Assignments”,|
|`126`||<https://www.mipi.org/MIPI_I3C_device_characteristics_register>|
|`127`|[MIPI05]|_MIPI Alliance I3C Application Note: General Topics_, App Note version 1.2,|
|`128`||MIPI Alliance, Inc., 6 June 2025 (MIPI Board approved 29 August 2025).|
|`129`|[MIPI06]|_MIPI Alliance Specification for Debug Over I3CTM_, version 1.1,|
|`130`||MIPI Alliance, Inc., 1 February 2024 (MIPI Board Adopted 26 May 2024).|



Copyright © 2021–2025 MIPI Alliance, Inc. **Public Release Edition** 

4 

App Note Version 1.2 29-Aug-2025 

I3C Application Note: Virtual Devices and Virtual Targets 

## `131` **4 Overview** 

`132` This Application Note describes several broad categories of information for Virtual Devices and Virtual `133` Targets: 

- `134` • Details of a few typical and supported capabilities, including different advanced capabilities. This `135` covers the allowances and challenges presented by each such set of capabilities. 

- `136` • Details of added functionality for such capabilities, including the set of which features are `137` typically integrated together (i.e., used in concert) to build a typical, coherent use case. 

- `138` • Integration aspects that are relevant for system designers and hardware/software integrators who `139` need to make use of these capabilities, in order to enable a particular use case or present such `140` capabilities to another Host using I3C. 

## `141` **4.1 Supported Capabilities** 

`142` Readers developing aspects of such I3C-based systems should consult the relevant sections of this `143` Application Note, which are intended to help avoid mistakes and to provide guidance not found in the I3C `144` Specification _**[MIPI03]**_ . 

`145` Analysis data is provided to help understand the use cases and impacts of choosing to implement certain `146` advanced capabilities relating Virtual Target behavior in a MIPI I3C Device. This analysis data could be used, `147` for example, when choosing what features and capabilities to integrate into advanced I3C Devices that expose `148` Virtual Targets on an I3C Bus, or into I3C Devices that bridge, present, or otherwise expose other downstream `149` entities to an I3C Bus via standard I3C Read/Write transfers and/or CCCs using a given I3C content protocol. 

`150` It is anticipated that the nature of such I3C Devices, their use cases for a particular application, and the `151` specific I3C content protocol chosen to access them might vary substantially. Implementers could make `152` different choices for a particular implementation, due to the nature of the functionality that is exposed, or the `153` aspects of downstream entities (i.e., devices on another bus, fabric or other interconnect) that are presented `154` or virtualized as Virtual Targets. However, the core concepts of Virtual Target capabilities remain largely the `155` same across the different classes of I3C Devices that expose or present Virtual Target capabilities or other `156` similar I3C Device virtualization techniques that are described in this Application Note. 

Copyright © 2021–2025 MIPI Alliance, Inc. **Public Release Edition** 

I3C Application Note: Virtual Devices and Virtual Targets 

App Note Version 1.2 29-Aug-2025 

## `157` **4.2 Using Added Functionality** 

`158` The I3C Specification _**[MIPI03]**_ includes optional extended functionality and the flexibility to allow for `159` different use cases. Some of these use cases have implications for the System Designer and for software on `160` the Controller. 

`161` The I3C Specification is focused on how each feature works from a protocol perspective; by contrast, this `162` Application Note provides additional information on how that feature can be incorporated into a system. This `163` additional information guides both assessments of whether it will be possible to accomplish what is wanted, `164` as well as how to accomplish it. 

- `165` 

Examples: 

- `166` • Offering electrical guidance on simple Devices that integrate multiple I3C Targets (i.e., with no `167` advanced capabilities or features) 

- `168` • Defining the various types of buffers, queues, or other structures recommended or required in `169` Shared Peripheral Logic for a composite I3C Device that presents multiple I3C Targets on the Bus, `170` and allows an I3C Controller to interact with the I3C Targets using an I3C content protocol 

- `171` • Understanding how the Target Reset Pattern and RSTACT CCC can be used to selectively reset `172` certain functions or “endpoints” within an advanced I3C Device, and defining which Target Reset `173` actions affect which internal entities or logic in such an I3C Device that presents multiple Virtual `174` Targets 

- `175` • Providing guidance on how Group Addresses and/or Multi-Lane configuration affects an I3C `176` Device that supports and presents multiple I3C Targets on the Bus 

- `177` • Enabling I3C Bridge Devices or I3C Routing Devices 

- `178` • Enabling I3C Hub Devices that have advanced capabilities and include at least one Virtual Target `179` that provides management of the Hub isolation circuitry 

Copyright © 2021–2025 MIPI Alliance, Inc. **Public Release Edition** 

6 

App Note Version 1.2 29-Aug-2025 

I3C Application Note: Virtual Devices and Virtual Targets 

## `180` **5 Virtual Target Concepts** 

- `181` This section discusses key guidelines that system integrators will want to follow, in order to implement `182` various types of I3C Devices that embody the concept of Virtual Devices. 

## `183` 

**Table 1 Section 5 Subjects** 

|**Table 1 Section 5 Subjects**||
|---|---|
|**Subject**|**Section**|
|Simple Integrated I3C Devices with Virtual Targets|**_5.1_**|
|Composite I3C Devices presenting Virtual Targets|**_5.2_**|
|I3C Bridge Devices|**_6.2_**|
|I3C Routing Devices|**_6.3_**|
|I3C Hub Devices with advanced isolation capabilities|**_6.4_**|



`184` The configuration of a given I3C Bus will depend upon the characteristics of the I3C Devices intended to be `185` active on that I3C Bus, as well as the use cases that drive the need for particular I3C Devices that expose or `186` present Virtual Targets. For I3C Devices that present Virtual Targets on an I3C Bus, many implementation `187` choices are possible, and this Application Note will interpret the requirements of Virtual Targets per the MIPI `188` I3C Specification. This Application Note will also show the most common options as well as `189` recommendations that can be applied to different situations. 

`190` _**Figure 1**_ shows an example I3C Bus that contains a variety of I3C Devices that embody or present Virtual `191` Targets, of the following types: 

- `192` • **Simple integrated I3C Devices** with multiple Virtual Targets in a single unit such as a die, stack, `193` or package (shown in the color purple) 

- `194` • **Composite I3C Devices** using Shared Peripheral logic to present multiple Virtual Targets (shown `195` in the color pink) 

- `196` • **I3C Bridge Devices** that expose bridged Targets (i.e., to a different bus such as I[2] C or SPI) where `197` each bridged endpoint is presented as an individual Virtual Target 

- `198` • **I3C Routing Devices** that enable transactions to/from other I3C Buses, with each Downstream `199` Bus segment exposed as a separate Virtual Target to which the I3C Controller can send Private `200` Write/Read transactions 

- `201` • **I3C Hub Devices** that provide electrical isolation for some I3C Targets on a Downstream I3C Bus `202` Segment, but that do not change the fundamental nature of the I3C Bus protocol that the I3C `203` Controller uses for transactions to/from these I3C Targets 

Copyright © 2021–2025 MIPI Alliance, Inc. **Public Release Edition** 

7 

I3C Application Note: Virtual Devices and Virtual Targets 

App Note Version 1.2 29-Aug-2025 

**==> picture [536 x 332] intentionally omitted <==**

**----- Start of picture text -----**<br>
I3C I3C<br>TARGET TARGET<br>Isolated Segment<br>I3C I3C<br>TARGETI3C I3C HUB ROUTING I3C TARGET TARGET<br>(isolating) DEVICE<br>Downstream Bus Segment<br>SDA<br>I3C<br>PRIMARY<br>CONTROLLER SCL<br>ACTIVE<br>Endpoint<br>I3C DEVICE (Integrated Package)<br>SHARED PERIPHERAL I3C<br>BRIDGE<br>DEVICE<br>I3C I3C I3C I3C Endpoint<br>VIRTUAL VIRTUAL<br>TARGET TARGET<br>TARGET TARGET<br>Bridged Endpoints<br>**----- End of picture text -----**<br>


## **LEGEND** 

**==> picture [319 x 29] intentionally omitted <==**

**----- Start of picture text -----**<br>
I3C CONTROLLER I3C DEVICE I3C DEVICE<br>I3C TARGET<br>(incl. Primary) (Integrated) (Virtualized)<br>**----- End of picture text -----**<br>


**Figure 1 I3C Bus with I3C Devices and Virtual Targets** 

```
204
```

Copyright © 2021–2025 MIPI Alliance, Inc. **Public Release Edition** 

8 

App Note Version 1.2 29-Aug-2025 

I3C Application Note: Virtual Devices and Virtual Targets 

## `205` **5.1 Simple Integrated I3C Devices** 

- `206` Virtual Targets inside an I3C Device can be a simple integration of multiple I3C Target Devices that exist `207` within the same physical unit or component, such as a replicated die, a die/wafer stack, or an integrated `208` package. This integration relies on different methods that can combine multiple such units together, for the `209` purpose of taking existing I3C Device implementations and bundling them together. Such steps could be `210` taken to save space, to reduce physical integration costs, or to meet other platform design considerations `211` without requiring a full re-design of existing I3C Device logic. 

- `212` The specific nature of the integration method does not matter for this Application Note, but the core concepts `213` below apply for any of the methods: 

- `214` • Each I3C Target Device might otherwise exist in a separate instantiation, if it were manufactured `215` and packaged separately (i.e., in a unit that included this I3C Device alone without other such I3C `216` Devices). 

- `217` • Each I3C Target Device could be separable from the other I3C Devices, and would neither expose `218` nor rely on any other, more advanced Virtual Target capabilities (i.e., those described in other `219` sections of this Application Note). 

- `220` For many I3C Devices that present such Virtual Targets, the simple integration model is well suited to reusing `221` existing I3C Device logic that can be packaged into a new form factor by a component designer. 

Copyright © 2021–2025 MIPI Alliance, Inc. **Public Release Edition** 

I3C Application Note: Virtual Devices and Virtual Targets 

App Note Version 1.2 29-Aug-2025 

## `222` **5.1.1 Internal Topologies** 

- `223` For use cases that rely on existing I3C Device logic, a simple integration could consist of various types of `224` I3C Devices that act as I3C Targets within the same unit as an integrated (i.e., combined) Device. In this `225` manner, each I3C Target is a Virtual Target because it resides within the same physical Device, but does not `226` necessarily possess any additional advanced functionality, nor advertise any additional Virtual Target `227` capabilities on an I3C Bus. 

- `228` There could be various topologies for such an integration. As examples, several models for topologies are `229` provided: 

- `230` • An I3C Bus that includes one such integrated I3C Device with multiple Virtual Targets could be `231` similar to a “Star-on-Stick” Bus topology, as described in _**Section 5.4**_ of the _**I3C Application**_ `232` _**Note: General Topics [MIPI05]**_ . 

- `233` • An I3C Bus that includes one such integrated I3C Device with multiple Virtual Targets could be `234` similar to a “Daisy-Chain” Bus topology, as described in _**Section 5.4**_ of the _**I3C Application Note:**_ `235` _**General Topics [MIPI05]**_ . 

- `236` Since all such Virtual Targets reside within the same physical unit, the internal distances (i.e., L2 and/or L3) `237` can be expected to be considerably shorter than external distance L1 (i.e., the distance from the I3C Controller `238` to the integrated I3C Device), and the “stub” distances to each individual Virtual Targets are directly `239` controlled by the component designer. 

- `240` • For integrations that consist of multiple existing silicon layouts (i.e., “hard IPs”) that are printed or `241` replicated onto the same combined die, the internal distances and stub properties are directly based `242` on the trace lengths between the pads in the combined die. However, the on-die traces or `243` additional routes might not necessarily be replicated, and in some cases might need to be specially `244` designed and integrated; whereas the “hard IPs” for the I3C Targets will likely be simple to `245` replicate (see _**Figure 2**_ ). 

- `246` • For integrations that consist of multiple wafers or dies that are printed or layered into a vertical `247` stack, the internal distances and stub properties are a function of the die stacking parameters, `248` which include the spacing distance as well as the type of die interconnect methods (e.g., wire `249` bonding, see _**Figure 3**_ ). 

- `250` • For integrations that consist of multiple dies within a package that are joined with various die-to- `251` die interconnects that might take the form of bridges, interposers, or simple wires, the internal `252` distances and stub properties are a function of the overall distance across such interconnects, `253` which could be considerably longer than the other two examples above, and depend on the sizes of `254` the dies and the locations of the pads (see _**Figure 4**_ and _**Figure 5**_ ). 

- `255` _**Figure 2**_ through _**Figure 5**_ illustrate examples of I3C Devices using each of the integration methods `256` mentioned above and in Table 2. 

Copyright © 2021–2025 MIPI Alliance, Inc. **Public Release Edition** 

10 

App Note Version 1.2 29-Aug-2025 

I3C Application Note: Virtual Devices and Virtual Targets 

```
257
```

**==> picture [260 x 238] intentionally omitted <==**

**----- Start of picture text -----**<br>
SDA<br>I3C<br>PRIMARY<br>CONTROLLER SCL<br>ACTIVE<br>PWR<br>GND<br>On-die<br>traces or<br>routes<br>I3C Target  I3C Target  not shown<br>(hard IP) (hard IP)<br>I3C DEVICE<br>(Replicated die using multiple hard IPs)<br>LEGEND<br>I3C CONTROLLER I3C DEVICE<br>(Primary) (Integrated)<br>**----- End of picture text -----**<br>


**Figure 2 Integrated I3C Device with Targets as Hard IPs on a Die** 

```
258
```

**==> picture [222 x 237] intentionally omitted <==**

**----- Start of picture text -----**<br>
SDA<br>I3C<br>PRIMARY<br>CONTROLLER SCL<br>ACTIVE<br>PWR<br>GND<br>I3C<br>I3CTARGET<br>I3CTARGET<br>TARGET<br>I3C DEVICE<br>(Stacked dies or wafers)<br>LEGEND<br>I3C CONTROLLER I3C DEVICE<br>(Primary) (Integrated)<br>**----- End of picture text -----**<br>


**Figure 3 Integrated I3C Device with Targets as Stacked Dies or Wafers** 

Copyright © 2021–2025 MIPI Alliance, Inc. **Public Release Edition** 

11 

I3C Application Note: Virtual Devices and Virtual Targets 

App Note Version 1.2 29-Aug-2025 

```
259
```

**==> picture [223 x 238] intentionally omitted <==**

**----- Start of picture text -----**<br>
SDA<br>I3C<br>PRIMARY<br>CONTROLLER SCL<br>ACTIVE<br>PWR<br>GND<br>I3C I3C<br>TARGET TARGET<br>I3C DEVICE<br>(Multiple dies using wires<br>as interconnects)<br>LEGEND<br>I3C CONTROLLER I3C DEVICE<br>(Primary) (Integrated)<br>**----- End of picture text -----**<br>


**==> picture [436 x 11] intentionally omitted <==**

**----- Start of picture text -----**<br>
260  Figure 4 Integrated I3C Device with Targets Connected by Wire Interconnects<br>**----- End of picture text -----**<br>


```
261
```

**==> picture [223 x 232] intentionally omitted <==**

**----- Start of picture text -----**<br>
SDA<br>I3C<br>PRIMARY<br>CONTROLLER SCL<br>ACTIVE<br>PWR<br>GND<br>I3C I3C<br>TARGET TARGET<br>BRIDGE<br>I3C DEVICE<br>(Multiple dies using<br>bridge or interposer)<br>LEGEND<br>I3C CONTROLLER I3C DEVICE<br>(Primary) (Integrated)<br>**----- End of picture text -----**<br>


**Figure 5 Integrated I3C Device with Targets Connected by Bridge or Interposer** 

`262` Each of these integration methods offers various advantages, but also poses different challenges as shown in `263` _**Table 2**_ . 

Copyright © 2021–2025 MIPI Alliance, Inc. **Public Release Edition** 

12 

App Note Version 1.2 29-Aug-2025 

I3C Application Note: Virtual Devices and Virtual Targets 

```
264
```

**Table 2 Comparison of I3C Device Integration Methods for Virtual Targets** 

|**Integration**<br>**Method**|**Advantages**|**Challenges**|
|---|---|---|
|**Hard IPs**<br>**in Same Dies**<br>**_Figure 2_**|•Allows reuse of existing verified<br>hardened IPs<br>•On-die traces or routes provide more<br>control over signal integrity|•Could require silicon re-verification<br>based on foundry process<br>•Some hard IPs might not be<br>compatible on same foundry process<br>•Always requires new metal layers for<br>on-die traces or routes between dies<br>and pads|
|**Stacked Dies**<br>**or Wafers**<br>**_Figure 3_**|•Works well for horizontally-constrained<br>applications, or other situations where<br>existing dies/wafers have been proven|•Die/wafer thickness impacts vertical<br>stack growth<br>•Possible interactions between<br>individual dies/wafers in Z-axis<br>•Requires planning for die/wafer<br>attachment|
|**Multiple Dies**<br>**using Wire**<br>**Interconnects**<br>**_Figure 4_**|•Simplest integration method for<br>existing I3C Targets<br>•Can unite dies from diverse foundry<br>processes or varying functions|•Differing die sizes could prevent<br>space-efficient integrations (in X-axis<br>or Y-axis)<br>•Wire lengths and stub properties could<br>be longer than with other methods|
|**Multiple Dies**<br>**using Bridge or**<br>**Interposer**<br>**_Figure 5_**|•Well-suited for larger integrations that<br>also integrate other functionality (i.e.,<br>other than I3C Targets) and already<br>need package and substrate design|•Some dies might require pads that are<br>suited for bridge or interposer<br>connections, based on package and<br>substrate choices|



## `265` 

## _**Note:**_ 

`266` _If an I3C Bus includes multiple I3C Devices that approach the example topologies or embody the_ `267` _above die design methodologies for integrated Virtual Targets, then the overall topology becomes_ `268` _more complex, i.e., a combination of either “Star-on-Stick” or “Daisy-Chain” for the I3C Devices_ `269` _containing such Virtual Targets. In such cases, the overall I3C Bus topology could be more complex_ `270` _to model. However, the effects of such combined topologies are not expected to be significant, since_ `271` _the internal distances can be expected to be shorter than other methods of system design (i.e.,_ `272` _boards or modules) and the “stub” properties can be understood and constrained by the component_ `273` _designer._ 

## `274` **5.1.2 Number of Virtual Targets in a Unit** 

`275` Version 1.0 and version 1.1 of the I3C Specification specified that an I3C Bus could support up to 11 I3C `276` Target Devices, based on typical electrical parameters including trace length and capacitive load for each `277` separate Target Device. However, version 1.2 of the I3C Specification does not have this limit (see _**[MIPI03]**_ `278` at _**Section 3.2.2**_ ) and does not specify a maximum limit of I3C Target Devices. (The limit was removed in `279` I3C v1.1.1.) Component designers can calculate and publish the appropriate electrical parameters when `280` designing integrated I3C Devices with multiple Virtual Targets, and System Designers should use these `281` parameters to guide the overall system design of the I3C Bus. 

Copyright © 2021–2025 MIPI Alliance, Inc. **Public Release Edition** 

13 

I3C Application Note: Virtual Devices and Virtual Targets 

App Note Version 1.2 29-Aug-2025 

## `282` **5.1.3 Virtual Target Power Management** 

- `283` If multiple Virtual Targets reside within the same unit, and if each Target could theoretically have been `284` packaged into its own separately I3C Device, then the integrated unit could also have per-Virtual Target `285` power management capabilities, with varying levels of granularity as needed. 

- `286` For example, the following optional capabilities could be implemented, at the discretion of the component `287` designer: 

- `288` • Separate power pins for each individual Virtual Target 

- `289` • Global power pins providing power for all Virtual Targets 

- `290` • Shared power pins providing power for some Virtual Targets, with other Virtual Targets powered `291` by other pins (i.e., either separate, shared, or global) 

- `292` • Global/shared power pins to the unit, with power management logic that provides direct power `293` control for one or more individual Virtual Targets, based on out-of-band direct pin inputs (i.e., `294` signals sent from another control unit or Application Host) 

- `295` • Global/shared power pins to the unit, with power management logic that provides automatic `296` power control for one or more individual Virtual Targets, based on system conditions or `297` Application Host configuration 

- `298` • Global/shared power pins to the unit, with one Virtual Target providing in-band mechanisms to `299` change the power states for the other Virtual Targets in the same unit, using I3C transactions to `300` control power management logic (i.e., Private Writes/Reads or CCCs) 

## `301` **5.1.4 Bus Configuration Registers** 

- `302` The I3C Specification states that each Virtual Target shall have a Bus Configuration Register (BCR) that `303` accurately describes its own configuration and capabilities (see _**[MIPI03]**_ at _**Section 4.3.1.2**_ ). 

- `304` Since a simple integrated I3C Device contains existing Target logic that has been instantiated with a new `305` integration, each Virtual Target does not necessarily need to report any advanced Virtual Target capabilities `306` using BCR Bit[4]. As a result, each of the Virtual Targets inside an integrated I3C Device will typically set `307` BCR Bit[4] to **1'b0** , unless: 

- `308` • An individual Virtual Target is a Bridge Device (per version 1.0 of the I3C specification) and `309` supports the SETBRGTGT CCC (see _**[MIPI03]**_ at _**Section 4.3.7.3.17**_ ). 

- `310` • An individual Virtual Target supports advanced Virtual Target capabilities (per version 1.1+ of the `311` I3C Specification), including but not limited to Bridging, Routing, or exposing other Downstream `312` Targets (i.e., advertising as a VT-capable Device, per _**[MIPI03]**_ at _**Section 4.3.7.3.19**_ ). 

- `313` _**Note:**_ 

`314` _The meaning and interpretation of BCR Bit[4] changed between version 1.0 and version 1.1+ of the_ `315` _I3C Specification. Starting with version 1.1+, BCR Bit[4] indicates support for one of several types of_ `316` _Virtual Target capabilities; see_ _**[MIPI03]** at_ _**Section 4.3.1.2.1** for more details. The I3C Controller can_ `317` _determine whether a Virtual Target supports I3C version 1.1+ by reading BCR Bit[5] and by using the_ `318` _GETCAPS CCC, per_ _**[MIPI03]** at_ _**Section 4.3.7.3.19** ._ 

Copyright © 2021–2025 MIPI Alliance, Inc. **Public Release Edition** 

14 

App Note Version 1.2 29-Aug-2025 

I3C Application Note: Virtual Devices and Virtual Targets 

## `319` **5.1.5 Dynamic Address Assignment and Provisioned ID Management** 

- `320` If a simple integrated I3C Device contains Virtual Targets that also support Dynamic Address Assignment 

- `321` with ENTDAA, then the component designer must ensure that each Target has been assigned a unique 48-bit `322` Provisioned ID. However, it could become a challenge to ensure that the Provisioned IDs are truly unique `323` across: 

- `324` • All Virtual Targets within the integrated I3C Device, and 

- `325` 

   - All I3C Devices in the system (i.e., the entire I3C Bus). 

- `326` The I3C Specification defines the requirements (see _**[MIPI03]**_ at _**Section 4.3.4.1**_ ) for I3C Targets, including `327` the need for a unique 48-bit Provisioned ID for each I3C Target on the I3C Bus. However, the Specification 

- `328` does not specify how to accomplish this, especially for Virtual Targets. This Application Note suggests `329` several methods for ensuring uniqueness, both within the integrated I3C Device and across the I3C Bus that `330` contains such an I3C Device (i.e., one or more instances). 

`331` For the 48-bit Provisioned ID values, the following fields are recommended for use by the Virtual Targets `332` within an integrated I3C Device: 

- `333` 

- `334` 

   - **Bits[31:16]:** Part ID 

   - **Bits[15:12]:** Instance ID (preferred for this use) 

- `335` • **Bits[11:0]:** Available for definition by the I3C Target implementer 

`336` Below are five strategies that could be used, either separately or together, to set the various portions of the `337` 48-bit Provisioned ID for the Virtual Targets within an integrated I3C Device. 

## `338` **5.1.5.1 Strategy 1** 

`339` This strategy typically works well for diverse Virtual Targets, or for Virtual Targets that might not all originate `340` from the same MIPI Manufacturer. 

`341` **Strategy:** Set(s) of external pins that provide direct input for some or all of the recommended fields of the `342` 48-bit Provisioned ID, to be directly pulled High or Low by the platform, as either 1'b1 or 1'b0 values. 

- `343` • Common set of direct pins that apply to all Virtual Targets 

- `344` 

   - Shared set of direct pins that apply to some Virtual Targets 

- `345` • Individual set of direct pins that only apply to one Virtual Target 

- `346` 

## **5.1.5.2** 

## **Strategy 2** 

`347` This strategy typically works well for Virtual Targets with similar characteristics, or that are identical in `348` nature and capabilities. 

`349` **Strategy:** Set(s) of external pins that control internal logic within the I3C Device, as indirect configuration `350` inputs recalling “presets” or various stored combinations of some or all of the recommended fields of the `351` 48-bit Provisioned ID. In this case, the internal logic would cause the affected Virtual Target’s field bits to be `352` set to 1'b1 or 1'b0. However, some portions could be unaffected or unchanged. 

- `353` • Common configuration inputs that affect fields for all Virtual Targets 

- `354` 

   - Shared configuration inputs that affect fields for some Virtual Targets 

- `355` • Individual configuration inputs that only affect fields for one Virtual Target 

Copyright © 2021–2025 MIPI Alliance, Inc. **Public Release Edition** 

15 

I3C Application Note: Virtual Devices and Virtual Targets 

App Note Version 1.2 29-Aug-2025 

## `356` **5.1.5.3** 

## **Strategy 3** 

- `357` This strategy could be suitable for I3C Devices that typically need additional configuration before initializing `358` the Virtual Targets. 

- `359` **Strategy:** Internal logic within the integrated I3C Device to directly set some or all of the recommended 

- `360` fields of the 48-bit Provisioned ID, based on stored configuration (i.e., PROM) or some other configuration `361` received via bus or other channel. 

- `362` • Can configure some or all Virtual Targets, based on stored or received configuration. 

## `363` **5.1.5.4 Strategy 4** 

- `364` **Strategy:** Fixed configuration of some of the recommended fields of the 48-bit Provisioned ID, set by internal `365` circuitry. 

- `366` 

## _**Note:**_ 

- `367` _This strategy is of course not appropriate for all of such fields in the 48-bit Provisioned ID;_ `368` _obviously, such a decision would restrict an I3C Bus to only one of these I3C Devices that hard-_ `369` _coded its Virtual Targets to have fixed Provisioned IDs and could not be changed by any external_ `370` _means._ 

## `371` **5.1.5.5 Strategy 5** 

- `372` Any combination of strategies 1–4 above. 

Copyright © 2021–2025 MIPI Alliance, Inc. **Public Release Edition** 

16 

App Note Version 1.2 

I3C Application Note: Virtual Devices and Virtual Targets 

29-Aug-2025 

## `373` **5.2 Composite I3C Devices** 

`374` Virtual Targets within an I3C Device can also exist as separate functions or entities that are presented or `375` exposed by a composite I3C Device, using Shared Peripheral logic. The Shared Peripheral logic presents `376` each Virtual Target with its own Dynamic Address, and manages the low-level I3C transactions using shared `377` FIFOs or buffers and a common set of pads (i.e., per-Device GPIOs for SDA and SCL). 

- `378` While such an approach requires re-design of the logic to implement I3C Target functionality, one key `379` advantage of using a composite I3C Device with Shared Peripheral logic is that the electrical parameters can `380` be more carefully controlled within the composite I3C Device, rather than requiring the serial clock and data `381` signals to be routed within a die, chip, or package as with a Simple Integrated I3C Device (see _**Section 5.1.1**_ 

## `382` **5.2.1 Architectural Overview** 

`383` A composite I3C Device that presents Virtual Targets on the I3C Bus needs to act, work, and function as `384` though it contained multiple I3C Targets, and in all respects other than being a single I3C Device (i.e., with `385` electrical parameters of a single connection to the SCL and SDA lines) such functions must be `386` indistinguishable from the multiple separate but equivalent I3C Target Devices that would otherwise be `387` needed to provide the same functionality. 

- `388` 

_**Note:**_ 

- `389` _The sole exception to this requirement is that a composite I3C Device that advertises Virtual Target_ `390` _capabilities must support the Virtual Target Detect operation via the RSTACT CCC, as defined in_ `391` _**Section 5.2.2.4** below and in the I3C Specification_ _**[MIPI03]** at_ _**Section 4.3.7.3.23** . By contrast, the_ `392` _equivalent separate I3C Target Devices (i.e., non-Virtual Targets) would not support the Virtual Target_ `393` _Detect operation._ 

- `394` _**Figure 6**_ shows an example of a composite I3C Device that contains Shared Peripheral logic (see `395` _**Section 5.2.2**_ below) and presents multiple I3C Virtual Targets on an I3C Bus, in a manner that would 

- `396` 

otherwise not be seen as such by the I3C Controller. 

**==> picture [385 x 280] intentionally omitted <==**

**----- Start of picture text -----**<br>
SDA<br>I3C<br>PRIMARY<br>CONTROLLER SCL<br>ACTIVE<br>PWR<br>GND<br>I/O SHARED PERIPHERAL<br>Internal buses<br>or fabrics<br>to other<br>... Virtual  Virtual  application<br>Target #1 Target #2 logic<br>(logic or FW) (logic or FW)<br>=<br>=<br>I3C DEVICE<br>(with Shared Peripheral Logic)<br>LEGEND<br>I3C CONTROLLER I3C DEVICE<br>(Primary) (Composite)<br>Figure 6 Composite I3C Device with Virtual Targets and Shared Peripheral Logic<br>**----- End of picture text -----**<br>


`397` 

Copyright © 2021–2025 MIPI Alliance, Inc. 

17 

**Public Release Edition** 

I3C Application Note: Virtual Devices and Virtual Targets 

App Note Version 1.2 29-Aug-2025 

## `398` **5.2.2 Shared Peripheral Logic** 

- `399` From an electrical perspective, it is recommended that a composite I3C Device that presents multiple Virtual `400` Targets be implemented with a single set of pins connecting to pads within or adjacent to the Shared `401` Peripheral logic. This would empower the Shared Peripheral logic to respond to transactions on the I3C Bus. `402` The Shared Peripheral logic could contain most of the lower-level components normally associated with a `403` typical generic I3C Target Device (as shown in _**Figure 9**_ in version 1.2 of the I3C Specification _**[MIPI03]**_ `404` and would also have additional internal state and memory to support the presentation of multiple functions. `405` Each function would enable the Shared Peripheral logic to present a Virtual Target that could respond to `406` CCCs, Private Writes, and Private Reads. In many cases, the Shared Peripheral logic could handle some of `407` the basic CCCs regarding Bus Configuration and Dynamic Address Assignment. 

`408` The _**Figure 6**_ example above shows Shared Peripheral logic within a die or an SoC that also has an internal `409` bus or fabric containing application logic associated with one or more Virtual Targets. This application logic `410` might be entirely implemented in internal logic (i.e., all hardware), or it might also accept configuration in `411` the form of firmware and/or software. Once configured, the application logic would be capable of responding `412` to Private Write transactions sent from the I3C Controller, and preparing data to return via I3C Private Read `413` transactions (in the event that the I3C Controller initiates such a transaction). The Shared Peripheral logic `414` stores the Dynamic Addresses and optional Group Addresses assigned to each of the known Virtual Targets, `415` and uses its internal FIFOs or buffers to manage data for Private Write, Private Read, or CCC transaction `416` requests. 

## `417` **5.2.2.1 Hot-Join and Dynamic Address Assignment** 

- `418` Since the Shared Peripheral logic handles the low-level I3C Bus protocol communications, it must also match `419` the Address Header for any assigned Addresses (i.e., Dynamic Addresses or Group Addresses) and either `420` direct those transactions to the appropriate logic within the composite I3C Device, or else handle the `421` transactions with its own FIFOs or buffers. As a result, it needs to know all of the assigned Addresses for all `422` of the Virtual Targets, and it therefore makes sense for the Shared Peripheral Logic to handle Dynamic `423` Address Assignment for all Virtual Targets within the I3C Device. 

- `424` If the Shared Peripheral logic does so, then it manages the process of joining the I3C Bus (i.e., sending the `425` Hot-Join Request, per _**[MIPI03]**_ at _**Section 4.3.5**_ ) and participating in Dynamic Address Assignment for `426` every Virtual Target it presents or exposes to the I3C Controller. 

- `427` The Shared Peripheral logic can be designed to present all Virtual Targets as Hot-Joining the I3C Bus with a `428` single Hot-Join Request, with the expectation that they can all receive Dynamic Addresses from the `429` Controller in a single phase (if possible). To the I3C Controller, this would appear as though all Virtual Targets `430` received power and joined the I3C Bus at the same time. Alternately, the Shared Peripheral logic can be `431` designed to emit multiple Hot-Join Requests in various phases, presenting one or more new Virtual Targets `432` on the I3C Bus per phase (i.e., as though some Virtual Targets received power and joined the I3C Bus at a `433` later time than others). 

Copyright © 2021–2025 MIPI Alliance, Inc. **Public Release Edition** 

18 

App Note Version 1.2 

I3C Application Note: Virtual Devices and Virtual Targets 

29-Aug-2025 

## `434` **5.2.2.2 BCR Values and GETCAPS CCC Support** 

- `435` Depending on the specifics of the implementation of such a composite I3C Device, some I3C commands sent `436` to one such Virtual Target might have side effects on other Virtual Targets using this Shared Peripheral logic `437` (such as Target Resets). Therefore, it is often important for the I3C Controller to identify such Virtual Targets `438` as having Shared Peripheral logic, and to understand which operations will have impact on other Virtual `439` Targets within the composite I3C Device. 

- `440` For all Virtual Targets within such a composite I3C Device, the I3C Specification states that each Virtual `441` Target shall have a Bus Configuration Register (BCR) that accurately describes its own configuration and `442` capabilities (see _**[MIPI03]**_ at _**Section 4.3.1.2**_ ); and shall also support the GETCAPS Format 2 CCC with `443` Defining Byte VTCAPS (0x93), and return a message of at least one byte (i.e., the VTCAP1 byte, see `444` _**[MIPI03]**_ at _**Section 4.3.2.1.2**_ and _**Section 4.3.7.3.19**_ ). As such, the following conditions apply: 

- `445` • In this first byte (VTCAP1), Bits[2:0] have a value of **3'd5** to inform the Controller that this `446` Virtual Target is presented by Shared Peripheral logic. 

- `447` • Bit[4] will be set appropriately, to indicate whether certain configuration CCCs (e.g., `448` SETNEWDA, SETMRL) sent to one Virtual Target have side effects on other Virtual Targets `449` connected to the same Shared Peripheral logic (see _**[MIPI03]**_ at _**Section 4.3.7.3.19**_ ). If Bit[4] is `450` set to **1'b1** , then the implementer must provide this information in the documentation for such a `451` composite I3C Device, regarding which specific configuration CCCs have these side effects.. 

- `452` • Bit[5] will be set to **1'b1** to indicate that this Device also supports the Virtual Target Detect `453` operation using the RSTACT CCC, as specified in the I3C Specification (see _**[MIPI03]**_ at `454` _**Section 4.3.7.3.23**_ ). If BCR Bit[4] has a value of **1'b1** , then support for this operation is required `455` for all Virtual Target Devices using Shared Peripheral logic within such a composite I3C `456` Device. 

- `457` • If this Virtual Target returns additional bytes in the message for this CCC, then the format of these `458` bytes (e.g., VTCAP2) has not yet been specified for this Virtual Target type. 

`459` It is best for all Virtual Targets within the same composite I3C Device to return the same contents for the `460` GETCAPS Format 2 CCC with Defining Byte VTCAPS. 

- `461` Additionally, the Shared Peripheral logic might choose to report some or all Virtual Targets as Offline `462` Capable, by setting BCR Bit[3] to **1'b1** . This might be useful when simulating power management states, for `463` use cases when a particular Virtual Target needs to block incoming messages and the Shared Peripheral logic `464` chooses to NACK incoming I3C transactions based on the matched Address. 

Copyright © 2021–2025 MIPI Alliance, Inc. **Public Release Edition** 

19 

I3C Application Note: Virtual Devices and Virtual Targets 

App Note Version 1.2 29-Aug-2025 

## `465` **5.2.2.3 RSTACT CCC Support** 

- `466` System Designers working with multiple Virtual Targets with individual Dynamic Addresses using Shared `467` Peripheral logic (or similar designs) are advised to carefully consider the following implications for the `468` RSTACT CCC. 

## `469` **When using the RSTACT CCC as a Direct SET CCC:** 

- `470` • Using the RSTACT CCC with Defining Byte 0x01 to reset a Virtual Target’s I3C Peripheral logic `471` might interrupt access to that Virtual Target (i.e., anything exposed via a specific Dynamic `472` Address). Depending on the implementation of the Shared Peripheral, it might preserve enough of `473` its internal state and retain its Dynamic Address for that Virtual Target, despite this interruption; or `474` it might fully reset its internal state for that Virtual Target, after which it will need to participate in `475` Dynamic Address Assignment again. However, it is unlikely that any other Virtual Targets `476` connected to the same Shared Peripheral logic will be affected. 

- `477` • Using the RSTACT CCC with Defining Byte 0x02 to reset the whole Target (i.e., the whole chip) `478` could reset the entire Device, including all Virtual Targets presented by the shared Peripheral `479` logic. 

- `480` • If one Virtual Target enables Debug functionality and conforms to the MIPI Debug Over I3C `481` Specification _**[MIPI06]**_ , then it is unlikely that using the RSTACT CCC with Defining Byte 0x03 `482` to reset that Virtual Target’s Debug Network Adaptors will interrupt any other Virtual Target `483` functionality or access on the Shared Peripheral logic. Additionally, if the Debug functionality is `484` internally connected to other application logic within the Device (which might be exposed by `485` another application-specific Virtual Target), then that application logic will not be reset or `486` otherwise impacted by a Debug Network Adaptor Reset to the Debug-capable Virtual Target. 

## `487` 

## **When using the RSTACT CCC as a Broadcast CCC:** 

- `488` • The RSTACT CCC with various Defining Bytes will cause an equivalent reset operation to be `489` applied to all Virtual Targets as well as the Shared Peripheral Logic. The specific nature of the `490` reset operation will depend on the Defining Byte. In some cases this might cause all Dynamic `491` Addresses for all Virtual Targets to be reset, after which all Virtual Targets would need to `492` participate in Dynamic Address Assignment again. 

Copyright © 2021–2025 MIPI Alliance, Inc. **Public Release Edition** 

20 

App Note Version 1.2 29-Aug-2025 

I3C Application Note: Virtual Devices and Virtual Targets 

`493` _**Table 3**_ shows the application of the various Defining Byte values for the RSTACT CCC that can be used with either the Direct SET form or the Broadcast `494` form, and how the implementation of a Virtual Target capable Device should interpret these Defining Byte values. It is derived from _**Table 38**_ in the I3C `495` Specification _**[MIPI03]**_ . 

```
496
```

**Table 3 Application of RSTACT Defining Byte Values for Virtual Target Capable Devices** 

|**Defining**<br>**Byte Value**|**Description**<br>**(for standard I3C Target Device)**|**Direct SET CCC to a Virtual Target**|**Broadcast CCC**|
|---|---|---|---|
|**0x00**|**No Reset on Target Reset Pattern**|**No change**|**No change**|
|**0x01**|**Reset the I3C Peripheral Only**<br>(Default)|**Reset portions of the Shared Peripheral logic**<br>**associated with the indicated Virtual Target**<br>Might include a reset of this Dynamic Address|**Reset the entire Shared Peripheral for all Virtual**<br>**Targets presented by the same Device**<br>Might include a reset of all Dynamic Addresses for all<br>Virtual Targets|
|**0x02**|**Reset the Whole Target**|**Reset all logic associated the indicated Virtual Target**<br>Should not impact other Virtual Targets presented by this<br>same Device|**Reset the entire Device**<br>Should impact all Virtual Targets presented by this Device|
|**0x03**|**Debug Network Adaptor Reset**<br>The Target shall not reset the I3C<br>Peripheral (per I3C Specification at<br>**_Section 4.3.7.3.23_**)|**Reset all Debug Network Adaptors for the indicated**<br>**Virtual Target**<br>Does not reset any portion of the Shared Peripheral logic|**Reset all Debug Network Adaptors for all Virtual**<br>**Targets which are Debug-capable**<br>Does not reset any portion of the Shared Peripheral logic,<br>or have impact on any other Virtual Targets presented by<br>the same Device which are not Debug-capable|
|**0x04**|**Virtual Target Detect**<br>Documented in this Application<br>Note at**_Section 5.2.2.4_**|**Set flag to detect other Virtual Targets presented by**<br>**the same Device**<br>Does not initiate any reset actions|_No effect, since this Defining Byte is only supported with_<br>_Direct CCCs_|
|0x05–0x3F|Reserved by MIPI|_N/A_|_N/A_|
|0x40–0x7F|Reserved for Vendors and external<br>standards|_N/A_|_N/A_|
|0x80–0xFF|Not applicable to Direct SET CCC<br>or Broadcast CCC|_N/A_|_N/A_|



```
497
```

Copyright © 2021–2025 MIPI Alliance, Inc. 

21 

**Public Release Edition** 

I3C Application Note: Virtual Devices and Virtual Targets 

App Note Version 1.2 29-Aug-2025 

## `498` **5.2.2.4 Virtual Target Detect Operation** 

- `499` Although a Device implementer might choose to denote the association between multiple Virtual Targets `500` sharing the same Peripheral logic in a custom manner, a standard method provides for far easier detection `501` and association. Hence, in order to correctly associate all Virtual Targets sharing the same Peripheral logic, `502` such a Device will support the Virtual Target Detect operation described in the I3C Specification _**[MIPI03]**_ `503` at _**Section 4.3.7.3.19**_ . To use this Virtual Target Detect operation, the I3C Controller sends the RSTACT CCC `504` with Defining Bytes 0x04 and 0x84 (Specification _**Section 4.3.7.3.23**_ ) with any Dynamic Addresses that are `505` configured to any Virtual Targets presented by the composite I3C Devices. 

- `506` The Virtual Target Detect operation utilizes a single “flag” bit in the Shared Peripheral logic. The Controller `507` can set this flag by using the RSTACT CCC with Defining Byte 0x04 directed to any Dynamic Address `508` assigned to any Virtual Target (with Direct SET CCC) or confirm that the flag was set on the same Virtual `509` Target’s Dynamic Address (with Direct GET CCC). Once set, the flag can be tested on any other Virtual `510` Target’s Dynamic Address by using the RSTACT CCC with Defining Byte 0x04 (with Direct GET CCC). `511` For Virtual Targets whose shared Peripheral’s flag was set, each of them will return a value of 0x01 to indicate `512` that the flag in their shared Peripheral has been previously set. 

- `513` The Controller can clear the flag in the shared Peripheral by sending the RSTACT CCC with Defining Byte `514` 0x00, either as a Broadcast CCC to all Devices, or as a Direct CCC to all Devices including all Virtual Target `515` capable Devices which support the Virtual Target Detect operation. 

- `516` _**Note:**_ 

- `517` _To minimize the security risks of side-channel attacks, the Shared Peripheral logic can internally_ `518` _handle all Direct CCC accesses to RSTACT with Defining Byte 0x04, without notifying any application_ `519` _or debug logic in any Target-specific implementation which connects to the Shared Peripheral logic._ `520` _Additionally, the state of this shared flag must not be accessible to any Virtual Target’s application_ `521` _logic behind its Shared Peripheral logic; as a result, any messages on the Bus pertaining to setting,_ `522` _confirming, or clearing this shared flag must also not be passed to the Virtual Target’s application_ `523` _logic connected to this Shared Peripheral logic. See_ _**[MIPI03]** at_ _**Section 4.3.7.3.23** ._ 

`524` Since one or more Virtual Target capable Devices might independently connect to an I3C Bus, the following `525` procedure can be used to correctly identify and associate all Virtual Targets with Shared Peripheral logic, `526` using only their Dynamic Addresses and no other prior knowledge. 

Copyright © 2021–2025 MIPI Alliance, Inc. **Public Release Edition** 

22 

App Note Version 1.2 29-Aug-2025 

I3C Application Note: Virtual Devices and Virtual Targets 

## `527` **Detection Procedure** 

- `528` 1. Send a Broadcast RSTACT CCC with Defining Byte 0x00, which will clear the detect flags in all `529` Virtual Target capable Devices with Shared Peripheral logic. It will also disable the default Target `530` Reset option (which is acceptable during the Virtual Target detection procedure). 

- `531` 2. Assemble a temporary list L containing all Targets where BCR Bit[4] was previously found to `532` have a value of **1'b1** . If any Targets’ BCRs have not yet been read, now is the time to read them `533` and determine the value of Bit[4]. 

- `534` 3. Loop over all Targets in list L. 

- `535` 

   - For each Target T: 

- `536` A. Send a Direct GET RSTACT CCC with Defining Byte 0x84 to Target T, to detect whether this `537` Target also supports Defining Byte 0x04. 

- `538` 

   - If this request is NACK’d by Target T, then remove Target T from list L and continue. 

- `539` • If this request is ACK’d by Target T, but the response is 0x00, then remove Target T from list `540` L and continue. 

- `541` 4. Loop again over all Targets in list L. 

- `542` For each Target T: 

- `543` A. Send a Direct SET RSTACT CCC with Defining Byte 0x04 to Target T, to set the detect flag `544` in one such I3C Device that is Virtual Target capable, so that it appears in all Virtual Targets `545` sharing its Peripheral logic. 

- `546` i. If this request is NACK’d by the Target T, then remove Target T from list L, and go back `547` to step 4. 

- `548` ii. If this request is ACK’d by the Target T, then send a Direct GET RSTACT CCC with `549` Defining Byte 0x04 to the same Target T, and confirm that it returns a value of 0x01. 

- `550` • If it does not return 0x01, then the flag was not set. Retry from step 4.A. If this fails `551` again, then remove Target T from list L, and go back to step 4. 

- `552` • If it does return 0x01, then the flag was set. 

- `553` iii. Loop over all other Targets in list L (not including Target T). 

- `554` For each Target P: 

- `555` 1. Send a Direct GET RSTACT CCC with Defining Byte 0x04 to Target P, to read the `556` detect flag in its Peripheral logic. 

- `557` • If this request is NACK’d by Target P, then continue to the next device. 

- `558` • If this request is ACK’d by Target P and the value is 0x01, then Target P and `559` Target T must share the same Peripheral logic. Create an association between `560` them (i.e., mark Target P as a counterpart to Target T), remove Target P from list `561` L, and continue to the next device. 

- `562` • If this request is ACK’d by Target P but the value is 0x00, then Target P and `563` Target T must not share the same Peripheral logic. Continue to the next device. 

- `564` iv. At the end of the loop, record all found associations with Target T. 

- `565` v. Send another Broadcast RSTACT CCC with Defining Byte 0x00, to clear the detect flags `566` in all VS-capable Devices with Peripheral logic. 

- `567` vi. Remove Target T from list L. 

- `568` 5. Any Targets remaining in list L should be handled as exceptions, i.e., as Virtual Targets with no `569` corresponding counterparts. 

`570` By following this procedure, the Host system which connects to the Controller can associate all Virtual `571` Targets with Shared Peripheral logic, as linked to their counterpart Virtual Targets. As soon as any Target is `572` found to have its detect flag set (i.e., by the Direct GET CCC returning a known value), its association with `573` another Virtual Target (i.e., the Target that had its detect flag set by the Direct SET CCC) is recorded, and it `574` is removed from the temporary List (to shorten processing time). 

Copyright © 2021–2025 MIPI Alliance, Inc. **Public Release Edition** 

23 

I3C Application Note: Virtual Devices and Virtual Targets 

App Note Version 1.2 29-Aug-2025 

## `575` **5.2.3 Enabling Virtual Target Transactions** 

`576` If the Shared Peripheral logic is not able to fulfill a particular transaction request immediately, but is `577` configured to accept such a transaction request on behalf of a Virtual Target, then the Shared Peripheral Logic `578` can steer each transaction request to the appropriate Virtual Target. 

- `579` 

- `580` 

This Virtual Target might exist in one of several forms: 

   - Separate internal application logic, per Virtual Function; 

- `581` • A unique virtual “endpoint” per Virtual Function, that is presented based on internal configuration `582` of configurable application logic or other programmable elements; or 

- `583` • Configuration and/or data received from other external buses, fabrics, or execution units within the `584` die, SoC, or system (i.e., platform). 

`585` The Shared Peripheral Logic steers the transactions based on the matched Address in the Address Header `586` (i.e., the Dynamic Address or Group Address assigned to a Virtual Target), and transactions are handled `587` appropriately based on transaction type: 

- `588` • **For Write-type transfers,** the Shared Peripheral will accept (i.e., will ACK) the Write and then `589` receive data bytes on behalf of the Virtual Target; these data bytes will be queued in a FIFO or `590` buffer, and transferred to the application logic when appropriate. 

- `591` • **For Read-type transfers,** the Shared Peripheral could either: 

- `592` • Pre-cache response data from the application logic, for one or more expected Read-type `593` transfers having certain parameters, and then be ready to ACK a Read-type transfer request that `594` matches those same parameters; or 

- `595` • Initially reject (i.e., NACK) any Read-type transfer request for which it does not have data ready `596` to respond, and then initiate an internal request to the application logic to provide response data `597` for a subsequent Read-type transfer having the same parameters, with the expectation that the `598` I3C Controller would retry the transfer request, in anticipation of a successful result (i.e., an `599` ACK on the retry) 

Copyright © 2021–2025 MIPI Alliance, Inc. **Public Release Edition** 

24 

App Note Version 1.2 

I3C Application Note: Virtual Devices and Virtual Targets 

29-Aug-2025 

## `600` **5.2.3.1 Special Considerations for HDR Modes and Multi-Lane Transfers** 

- `601` 

## **HDR Modes** 

- `602` If a composite I3C Device with Shared Peripheral logic also supports any of the optional HDR Modes (per `603` _**[MIPI03]**_ at _**Section 6.1**_ through _**Section 6.4**_ ), then these could be mapped into additional higher-level `604` transactions as HDR WRITE or HDR READ commands, which can be steered to the specific logic within `605` the composite Device for a given Virtual Target, based on the matched Address in the HDR structured `606` protocol element (i.e., Command Word or Header Block). 

- `607` 

## _**Note:**_ 

- `608` _HDR Modes also support additional parameters and metadata per transaction request, such as HDR_ `609` _Command Bytes (per HDR Mode). As a result, the internal configuration of the Shared Peripheral_ `610` _logic must appropriately handle valid transaction requests with different HDR Command Byte values_ `611` _and other parameters, and must only ACK such a transaction if it can respond to such a supported_ `612` _transaction for which it is ready to send or receive data._ 

- `613` _If the Shared Peripheral logic receives a transfer with an HDR Command Byte or other parameters_ `614` _that are not supported, then the Shared Peripheral logic must NACK the transaction request._ 

- `615` 

## **Multi-Lane Transfers** 

`616` If a composite I3C Device with Shared Peripheral logic also supports Multi-Lane transfers, then it will use `617` the correct Multi-Lane configuration (i.e., for supported I3C Modes) based on the Dynamic Address or Group `618` Address for each transfer in that I3C Mode. 

- `619` • **In HDR-DDR and HDR-TSP Modes:** The current Multi-Lane configuration does not affect the way `620` that the Shared Peripheral logic must parse the Address field of every transaction, since all Data `621` Transfer Codings use SDA[0] only to transmit the Address for the HDR Command Word for `622` Multi-Lane transfers (i.e., the same as for single-Lane transfers in the same HDR Mode). 

- `623` • **In HDR-BT Mode:** The current Multi-Lane configuration affects the way that the Shared Peripheral `624` logic must parse the Address field of every transaction, per the I3C Specification (see _**[MIPI03]**_ at `625` _**Section 6.7.3.5.3**_ ). This is a consequence of selecting a Data Transfer Coding that uses the `626` additional Data Lanes (i.e., SDA[1–3]) since HDR-BT Mode defines a different bit packing format `627` for these alternate Data Transfer Codings, and this changes how the Shared Peripheral logic must `628` parse the Address field of the HDR-BT Header Block. 

- `629` • If such alternate Data Transfer Codings are used, then the I3C Controller and all HDR-BT `630` capable I3C Devices must agree to use the same interpretation and bit packing format for `631` HDR-BT Header Blocksin order to correctly parse the Address field of every transaction in `632` HDR-BT Mode. If this agreement is not achieved, then communication errors are likely to `633` happen. 

- `634` • If an HDR-BT capable composite I3C Device cannot support (or is not configured to support) `635` such an alternate Data Transfer Coding, or if there is a mismatch between the Data Transfer `636` Coding that the I3C Controller uses and the Data Transfer Coding that such a composite I3C `637` Device is configured to expect, then there will be communication errors on the I3C Bus. For `638` example, the composite I3C Device will likely misunderstand the data that the I3C Controller `639` drives on SDA[0] and any additional Data Lanes (i.e., SDA[1–3]) during the HDR-BT Header `640` Block. This will likely lead to incorrectly matched Addresses or mistaken ACKs at the wrong `641` time, for Address values that were interpreted incorrectly (i.e., differently than the I3C `642` Controller intended to drive) across any of the Data Lanes. 

Copyright © 2021–2025 MIPI Alliance, Inc. **Public Release Edition** 

25 

I3C Application Note: Virtual Devices and Virtual Targets 

App Note Version 1.2 29-Aug-2025 

## `643` **6 Connecting to Other Buses via I3C Virtual Targets** 

## `644` **6.1 Common Concepts** 

- `645` Bridge Devices ( _**Section 6.2**_ below) and Routing Devices ( _**Section 6.3**_ below) share many similarities: they `646` present one or more Virtual Target devices to an I3C Bus, and they handle transactions to and from these `647` Downstream targets using assigned Dynamic Addresses. 

`648` **For Bridge Devices,** the Downstream targets are not on an I3C Bus, but the Bridge Device presents its `649` bridged endpoints to the Upstream I3C Bus as individual Virtual Targets. Each bridged endpoint has its own `650` Dynamic Address and can be addressed directly via Private Write/Read transfers. 

- `651` • The Downstream targets might connect via some other multi-drop bus, such as I[2] C or SMbus, and `652` might actually be individual devices on that bus, for which there would be a 1-to-1 mapping of `653` Dynamic Addresses. 

- `654` • Alternately, the Downstream targets might connect via another interface, such as SPI or UART, or `655` might use another signaling method implemented using an interface (e.g., GPIOs) in the Bridge `656` Device. For such a case, there might not always be multiple distinct targets on that other interface, `657` but their presence might be simulated or virtualized by the Bridge Device, based on the nature of `658` the communication protocol. 

- `659` • For more details about Bridge Devices, see _**Section 6.2**_ below. 

`660` **For Routing Devices,** the Downstream targets represent other I3C Bus Segments, and the Routing Device `661` typically acts as a Controller for those segments. 

- `662` • The Routing Device acts as a router that forwards Private Write transfers from the Upstream I3C `663` Bus Segment, to send the data payload to I3C Devices on the Downstream I3C Bus Segment. The `664` Routing device also performs the reverse for any corresponding data that will be read from I3C `665` Devices on the Downstream segment, typically taking the form of a Private Read transfer on the `666` Upstream segment. 

- `667` • A Routing Device can route transactions for one or more Downstream I3C Bus Segments, and `668` handles communications across the I3C Bus Segments. In order to determine which of the I3C `669` Devices on the Downstream segment to address, the I3C content protocol for the Routing Device `670` relies on some method of encapsulating or framing the Private Write and Private Read transfers. `671` This typically takes a structured format that includes the identifier or I3C Address for specific I3C `672` Devices on that Downstream segment. 

- `673` • However, the I3C Targets on the Downstream segments are not directly presented to the Upstream `674` segment (i.e., a different Dynamic Address is presented), and the Routing Device must store and `675` forward each transaction. The Routing Device can also use an In-Band Interrupt (IBI) Notification `676` on the Upstream segment to notify the I3C Controller that data is ready to be consumed for a `677` Private Read transaction from the Downstream segment. 

- `678` • For more details about Routing Devices, see _**Section 6.3**_ below. 

- `679` Additionally, I3C also enables new use cases for specialized Hub Devices. Hub Devices provide some `680` measure of electrical isolation between the Upstream I3C Bus Segment and the other I3C Target Devices on `681` a Downstream I3C Bus Segment. 

- `682` • Such a Hub Device might also present one or more Virtual Targets, if it allows for advanced `683` management of the circuitry that provides isolation, or if it manages the flow of transactions on `684` one or more Downstream segments. The Virtual Target might accept commands using CCCs `685` and/or Private Write/Read transfers to configure the Hub Device. 

- `686` • For more details about Hub Devices that use Virtual Targets, see _**Section 6.4**_ below. 

Copyright © 2021–2025 MIPI Alliance, Inc. **Public Release Edition** 

26 

App Note Version 1.2 29-Aug-2025 

I3C Application Note: Virtual Devices and Virtual Targets 

## `687` **6.1.1 Manager Function** 

- `688` Bridge Devices, Routing Devices, and specialized Hub Devices will provide at least one Virtual Target as a `689` Manager Function. This Manager Function allows the I3C Controller on the Upstream Bus segment to `690` configure the Device, to expose its capabilities, and optionally to configure its connections to Downstream `691` targets, bridged endpoints, or other types of Bus segments, depending on the Device type. 

- `692` Common capabilities of the Manager Function for such Devices will typically include: 

- `693` • Support for Dynamic Address Assignment with ENTDAA, using a unique 48-bit Provisioned ID `694` (i.e., as with any other typical I3C Target on the Upstream I3C Bus Segment) 

- `695` • Bus Configuration Register (BCR) and Device Configuration Register (DCR) values that expose `696` Virtual Target capabilities, because this Device presents or exposes other Downstream Virtual `697` Targets (depending on its type) 

- `698` • Presentation of the Manager Function as its own Virtual Function for configuration or control, in `699` addition to any other Virtual Targets based on functions that the Device might present (per its `700` type). 

- `701` • Peripheral logic that can accept and handle I3C transfers, including Private Write/Read transfers `702` and CCCs, to handle configuration and management via this Dynamic Address 

- `703` • If the Device supports I3C version 1.1 or greater, then this includes the GETCAPS Format 2 `704` CCC with Defining Byte VTCAPS (see _**[MIPI03]**_ at _**Section 4.3.7.3.19**_ ) 

- `705` • This might also include other required CCCs, such as RSTACT 

- `706` • Additional advanced logic that enables specific capabilities, and presents other Virtual Targets per `707` the use case (i.e., Bridging, Routing, or Hub) 

## `708` **6.1.2 Configuration of Downstream Virtual Targets** 

- `709` Bridge Devices and Routing Devices might automatically configure their Downstream targets or endpoints. `710` However, Hub Devices as described in this Application Note are not required to automatically configure their `711` Downstream I3C Targets. 

- `712` _**Note:**_ 

- `713` _Configuring such Targets or endpoints does not always mean they must be automatically exposed_ `714` _or presented on the Upstream I3C Bus Segment. For example, some Bridge Devices might configure_ `715` _their bridged endpoints with fixed configuration or directly-applied settings, but still rely on the I3C_ `716` _Controller to use the SETBRGTGT CCC to enable such bridged endpoints to appear on the I3C Bus_ `717` _as unique Virtual Targets with unique Dynamic Addresses. However, most internal configuration tasks_ `718` _are usually best left under the direct control of the Bridge Device itself._ 

- `719` For Bridge Devices and Routing Devices that automatically configure any Downstream targets, the Manager `720` Function could indicate this capability in the VTCAP2 byte (as returned from GETCAPS Format 2 CCC with `721` Defining Byte VTCAPS). If the Manager Function does not support a two-byte message for this CCC, then `722` the I3C Controller can assume that automatic configuration is the default. 

- `723` • For Bridge Devices, each bridged endpoint is a separate Virtual Target. It is essential that the `724` method for configuring a Downstream target be either built-in, configured directly to the Bridge `725` Device, or otherwise derived from the configuration sent by the Controller of the Upstream I3C `726` Bus Segment (i.e., the same Bus Configuration CCCs). Additional configuration steps might be `727` necessary, based on the specific Downstream bus or interface, as well as the Downstream Target or `728` endpoint that is being presented as a Virtual Device. 

- `729` This can be remapped into a format which is suitable for the type of Downstream interface, to the `730` extent that such CCCs can be mapped into the set of configuration commands which are possible. `731` However, this might not always be applicable for all such CCCs. 

- `732` • In some cases, the Bridge Device might need to perform automatic configuration of some modes `733` or request types, or might need to cache certain types of downstream segment events that have `734` not been configured, or that do not have a clean analogue to I3C configuration CCCs. The 

Copyright © 2021–2025 MIPI Alliance, Inc. **Public Release Edition** 

27 

I3C Application Note: Virtual Devices and Virtual Targets 

App Note Version 1.2 29-Aug-2025 

`735` Bridge Device typically defines and implements a method for mapping these events or `736` conditions into Private Read/Write transfers or In-Band Interrupts, but this is left to the `737` discretion of the implementer. 

- `738` • For Routing Devices, each Downstream target (i.e., an I3C Target Device connected to a `739` Downstream I3C Bus Segment) must be configured on that I3C Bus Segment. 

- `740` For most applications, this configuration will be derived from any Bus Configuration CCCs (e.g., `741` ENEC, DISEC, or SETBUSCON) that the Controller might have previously broadcast to all `742` Devices on the Upstream I3C Bus Segment, or that the Controller might have sent directly to this `743` Routing Device. For special use cases, the Controller might send special configuration to the `744` Routing Device, or the Routing Device might have internal configuration for its Downstream Bus `745` configuration. 

- `746` • The Routing Device could cache this configuration that might have been received from the `747` Controller; if so, it would replay it on any Downstream segments as needed, in order to `748` configure new Downstream I3C Target Devices that appear (or that Hot-Join, if Hot-Join is `749` supported). However, certain use cases involving the SETBUSCON CCC could rely on repeated `750` Broadcasts with different context bytes and optional data (as defined per the context byte) that `751` must be emitted in the correct order. (Refer to the SETBUSCON CCC, see _**[MIPI03]**_ at `752` _**Section 4.3.7.3.27**_ , “Layered Protocol Contexts”.) Such a Routing Device must be present on `753` the Bus to receive these Broadcasts, and upon receiving them it must cache them in the correct `754` order, based on the original intent as received from the Controller of the Upstream I3C Bus `755` Segment. 

- `756` • Alternately, the Routing Device could simply pass along some or all of these Bus Configuration `757` CCCs to downstream I3C Target Devices, as soon as they are sent by the Upstream I3C Bus `758` Segment’s Controller. In that case, the Routing Device can request the I3C Controller to re-send `759` all active and current configuration (i.e., what is most current) without relying on an internal `760` cache. However, the Routing Device might need to filter or block certain types of requests from `761` downstream Devices as they “join” the Bus, until the requested configuration has been received `762` and re-sent. 

- `763` Routing Devices that do not automatically configure any Downstream targets and that require the I3C `764` Controller on the Upstream I3C Bus Segment to configure every Downstream I3C Target Device are also `765` possible. For such Bus configurations, the Routing Device must transparently pass all Bus Configuration `766` CCCs to each new Downstream I3C Target Device once the I3C Controller is made aware of its presence on `767` the I3C Bus. The I3C Controller must also be prepared to repeatedly send these Bus Configuration CCCs `768` when a new Downstream target (presented by the Routing Device as a Virtual Target) is observed to join the `769` I3C Bus. 

- `770` Bridge Devices that do not automatically configure any Downstream bridged endpoints as Virtual Targets are `771` possible, but this option is not always recommended because the Bridge Device must rely on the I3C `772` Controller (i.e., in the Upstream I3C Bus Segment) to have perfect knowledge of the configuration of all such `773` bridged endpoints. 

Copyright © 2021–2025 MIPI Alliance, Inc. **Public Release Edition** 

28 

App Note Version 1.2 29-Aug-2025 

I3C Application Note: Virtual Devices and Virtual Targets 

## `774` **6.2 Bridge Devices** 

- `775` The MIPI I3C Specification _**[MIPI03]**_ covers inter-bus bridging support, both passively and actively. In all `776` cases, the bridged Targets (i.e., the Devices that are being bridged) are presented as Virtual Target devices, `777` each with its own I3C Dynamic Address. The bridged Targets can transact with the I3C Bus through the `778` Bridge Device. 

## `779` **6.2.1 Architectural Overview** 

`780` In many aspects, a Bridge Device is similar in concept to a composite I3C Device (see _**Section 5.2.1**_ above) `781` that uses Peripheral logic to present its Virtual Targets and interacts with its Upstream I3C Bus through its `782` additional capabilities (i.e., capabilities over and above those required of a simple I3C Target). 

`783` _**Figure 7**_ shows an example of an I3C Bridge Device that presents multiple I3C Virtual Targets on an I3C `784` Bus, where each Virtual Target is a representation or abstraction of one or more bridged endpoints on an `785` external Bus. In this example, the Bridge Device also has a Bridge Manager function as the primary Virtual `786` Target, used by the I3C Controller (i.e., on its Upstream I3C Bus Segment) to configure and manage the `787` Bridge Device and its presentation of the bridged Targets, the associated bridged Endpoints, and optionally `788` any controllable parameters associated with its external I/O to its Downstream bus or interface. 

```
789
```

**==> picture [426 x 262] intentionally omitted <==**

**----- Start of picture text -----**<br>
SDA<br>I3C<br>PRIMARY<br>CONTROLLER SCL<br>ACTIVE<br>PWR<br>GND Bridge<br>Manager<br>I/O PERIPHERAL Function<br>Virtual Targets<br>ID (MSB, LSB)<br>... Bridged  Bridged  Dynamic Address Endpoint #1<br>Target #1 Target #2<br>External I/O<br>Endpoint #2<br>I3C BRIDGE DEVICE<br>(with Peripheral Logic and External I/O)<br>LEGEND ...<br>Bridged Endpoints<br>I3C CONTROLLER I3C BRIDGE  I3C TARGET<br>(Primary) DEVICE (Virtual)<br>**----- End of picture text -----**<br>


**Figure 7 I3C Bridge Device with Virtual Targets and Bridged Endpoints** 

Copyright © 2021–2025 MIPI Alliance, Inc. **Public Release Edition** 

29 

I3C Application Note: Virtual Devices and Virtual Targets 

App Note Version 1.2 29-Aug-2025 

## `790` **6.2.2 Bridge Manager Function** 

- `791` Bridge Devices present at least one Bridge Manager Function as a Virtual Target. A Bridge Manager Function `792` exposes the Device’s presence on the I3C Bus and describes its capabilities and optional features (see `793` _**Section 6.1.1**_ above). 

- `794` _**Note:**_ 

- `795` _Previous versions of this Application Note used the term “Control Function” to describe the Virtual_ `796` _Target that provides management and control of the Bridge Device. This term has been replaced with_ `797` _“Manager Function” to avoid confusion with the new normative term “Controller”, see_ _**Section 2.1**_ `798` _above._ 

- `798` 

- `799` If such Devices are fully compliant with version 1.1+ of the I3C Specification _**[MIPI03]**_ , then they must `800` report this capability in the Bus Configuration Register (BCR) for the Manager Function’s Virtual Target. `801` Specifically, Bit[4] of the BCR for the Manager Function must indicate that it is a Virtual Target (see `802` _**[MIPI03]**_ at _**Section 4.3.1.2.1**_ ). Such Targets also typically support the GETCAPS Format 2 CCC with `803` Defining Byte VTCAPS (see _**[MIPI03]**_ at _**Section 4.3.7.3.19**_ ) to describe more details regarding the `804` capabilities and features of Bridge Devices. 

- `805` • Manager Functions for Bridge Devices will support the GETCAPS Format 2 CCC with Defining `806` Byte VTCAPS, and return a message of at least one byte, but preferably two bytes (i.e., both the `807` VTCAP1 byte and the VTCAP2 byte). 

- `808` • In the first byte (VTCAP1), Bits[2:0] will have a value of either **3'd1** or **3'd2** , depending on `809` whether the I3C Controller must use the SETBRGTGT CCC to configure the bridged targets as `810` Virtual Targets (see _**Section 6.2.3.1**_ below), vs. the Bridge Device will configure its bridged `811` targets automatically (see _**Section 6.2.3.2**_ below). 

- `812` • In the second byte (VTCAP2), the following fields will be set to reflect a Bridge Device: 

- `813` • Bits[1:0] will have either a value of **2'd2** if the Bridge Device can send an IBI for each `814` bridged target with its Target Address, or a value of **2'd0** if the Bridge Device does not `815` support IBIs from any bridged targets. 

- `816` _**Note:**_ 

- `817` _A value of_ _**2'd1** is not recommended for most Bridge Device implementations._ 

- `818` 

   - Bit[2] must have a value of **1'b1** . (A value of **1'b0** does not make sense for Bridge Devices.) 

- `819` • Bits[4:3] will generally have a value of **2'd0** , unless the Bridge Device requires more specific `820` configuration of its bridged targets with the help of Broadcast CCCs (such as SETBUSCON, `821` ENEC, or DISEC) and cannot accomplish the task without repeated reminders from the I3C `822` Controller. 

Copyright © 2021–2025 MIPI Alliance, Inc. **Public Release Edition** 

30 

App Note Version 1.2 29-Aug-2025 

I3C Application Note: Virtual Devices and Virtual Targets 

## `823` **6.2.3 Initialization and Configuration** `824` There are two general ways an I3C Bridge Device can get the bridged Virtual Targets configured with their `825` I3C Dynamic Addresses, and presented using its bridged endpoints: 

- `826` 1. The Host’s software or firmware knows what is physically attached to the Bridge Device, using `827` information provided by the System Designer (i.e., by table or otherwise), and uses the `828` SETBRGTGT CCC to inform the Bridge Device about each endpoint and its assigned Dynamic `829` Address. 

- `830` A. For Bridge Devices that comply with version 1.1+ of the I3C Specification, such a Bridge `831` Device exposes a Manager Function which advertises Virtual Target capabilities in its BCR `832` (see _**[MIPI03]**_ at _**Section 4.3.1.2.1**_ ) and indicates a Virtual Target Type **3'd1** in its VTCAP1 `833` data byte (see _**[MIPI03]**_ at _**Section 4.3.7.3.19**_ ). 

- `834` B. To configure the bridged Downstream Devices, the Controller sends the SETBRGTGT CCC `835` to the Manager Function (see _**Section 6.2.3.1**_ below). 

- `836` 2. The Bridge Device itself knows what is attached, and uses the ENTDAA CCC to represent each `837` one separately to the Controller, so that each bridged Target is assigned a unique Dynamic `838` Address. 

- `839` A. For Bridge Devices that comply with version 1.1+ of the I3C specification, such a Bridge `840` Device exposes a Manager Function which advertises Virtual Target capabilities in its BCR `841` (see _**[MIPI03]**_ at _**Section 4.3.1.2.1**_ ) and indicates a Virtual Target Type **3'd2** in its VTCAP1 `842` data byte (see _**[MIPI03]**_ at _**Section 4.3.7.3.19**_ ). 

- `843` B. The Controller does not need to explicitly configure the bridged Downstream Devices using `844` the SETBRGTGT CCC. 

- `845` 

## _**Note:**_ 

- `846` • _The Manager Function for the Bridge Device will have a Dynamic Address in the first case, and_ `847` _can optionally have its own Dynamic Address in the second case._ 

- `848` • _The Bridge could also be configured using some private contract between the Controller and the_ `849` _Bridge Device, and the model would likely be similar to the effect of the SETBRGTGT CCC: the_ `850` _Controller allocates a set of Dynamic Addresses. It could also be the case that the Controller_ `851` _programs the Bridge Device without searching for its initial bridged Targets (i.e., based on_ `852` _configuration received from the Host’s higher-level software) and then uses the ENTDAA CCC_ `853` _again to learn each target, whether by Controller decision or as the result of a subsequent_ `854` _Hot-Join Request._ 

- `855` • _Bridging in the other direction (i.e., from some other bus into an I3C Bus) would require a full I3C_ `856` _Controller implementation (i.e., a Secondary Controller), and would also require the I3C Active_ `857` _Controller to pass the Controller Role to the Bridge Device for some period of time. As a result,_ `858` _that would work the same as with any I3C Controller-capable Device._ 

Copyright © 2021–2025 MIPI Alliance, Inc. **Public Release Edition** 

31 

I3C Application Note: Virtual Devices and Virtual Targets 

App Note Version 1.2 29-Aug-2025 

## `859` **6.2.3.1 Use of SETBRGTGT (Set Bridge Targets)** 

- `860` An I3C Bridge Device might require use of the SETBRGTGT CCC (see I3C Specification, _**Section**_ `861` _**4.3.7.3.17**_ ) to configure the bridged Downstream Targets so they can be used on the I3C Bus. 

- `862` 

The steps to use the SETBRGTGT CCC are as follows: 

- `863` 1. The System Designer implants knowledge about the bridged endpoint’s Virtual Targets in the `864` Primary Controller’s firmware; this might be either an I3C HCI compliant Bus Controller, or an `865` I3C Bus Controller with a more direct Host interface. 

- `866` A. This can be a table, such as is used to capture knowledge about other I3C (and any legacy I[2] C) `867` Targets, or it can be handled in other ways. 

- `868` B. This would include the level of detail to indicate protocol, which pin-channels, etc., as `869` suitable for the ID[15:0] field of the SETBRGTGT CCC. 

- `870` 2. The Manager Function of the I3C Bridge Device participates in the normal I3C Dynamic Address `871` Assignment procedure, whether at Bus initialization or as the result of a Hot-Join Request. 

- `872` A. This means that the Manager Function might have a static address and either SETDASA or `873` SETAASA CCC would be used, or it might only respond to the ENTDAA CCC. 

- `874` • If Hot-Join is supported, then ENTDAA support is also required and the Manager `875` Function must also have an assigned 48-bit Provisioned ID (PID) and support the `876` GETPID CCC (see _**[MIPI03]**_ at _**Section 4.3.7.3.12**_ ). 

- `877` B. The Manager Function’s DCR value indicates its capabilities as a Virtual Target for a Bridge `878` Device, and its BCR value is that of a typical I3C Target. 

- `879` • For Bridge Devices that comply with version 1.1+ of the I3C specification, the `880` Manager Function’s BCR must have Bit[4] set to indicate Virtual Target capabilities `881` (see _**[MIPI03]**_ at _**Section 4.3.1.2.1**_ ), because the Bridge Device exposes other `882` Downstream Devices. 

- `883` C. If Dynamic Address Assignment with ENTDAA is supported, then the Manager Function will `884` have a normal MIPI Manufacturer ID and 48-bit PID (per _**[MIPI03]**_ at _**Section 4.3.4.1**_ ). 

- `885` • If more than one physical Bridge Device of the same manufacturer and type (i.e., `886` part ID) can be used on the same I3C Bus, then these must be unique on the I3C Bus `887` (as is the case for all I3C Targets), and the instance ID portion of the 48-bit PID can `888` be used to differentiate them. 

- `889` • The Manager Function must also support the GETPID CCC (see _**[MIPI03]**_ at `890` _**Section 4.3.7.3.12**_ ). 

- `891` D. The Manager Function’s assigned Dynamic Address is then used only for communication `892` between the Controller and the Manager Function itself. 

- `893` • For some use cases, the Controller might never use this Dynamic Address after initial `894` configuration of the bridged Targets. For other use cases, this Dynamic Address `895` might subsequently be used for such purposes as re-configuration, error handling, `896` etc. 

Copyright © 2021–2025 MIPI Alliance, Inc. **Public Release Edition** 

32 

App Note Version 1.2 29-Aug-2025 

I3C Application Note: Virtual Devices and Virtual Targets 

- `897` 3. After assigning a Dynamic Address to the Manager Function, the Controller will then use the `898` SETBRGTGT CCC with the Manager Function to configure the other Virtual Targets for the `899` Bridge Device’s bridged endpoints: 

- `900` A. The Bridge Device will assign a unique Dynamic Address for each target or endpoint that is `901` being bridged. It will use the ID[15:0] field of its 48-bit Provisioned ID to provide info for `902` each new Virtual Target for a bridged endpoint, as needed. 

- `903` • Since the Controller and Bridge device already know about the bridged endpoints, `904` and have shared understanding of the Dynamic Addresses that the Virtual Targets `905` will use, this Dynamic Address assignment process does not rely on the ENTDAA `906` CCC. 

- `907` B. The Bridge Device will likely set the BCR ‘limitations’ bit for these Virtual Targets. This `908` allows the Controller to interrogate these Virtual Targets to determine their maximum data `909` transfer limits, their read turnaround time delays, and to discover any other consideration(s). 

- `910` C. The Bridge Device can generate an IBI that originates from such a Virtual Target’s Dynamic `911` Address using the Peripheral logic. The Controller can use the GETBCR CCC during `912` configuration, to read how such a Bridge Device handles the IBI, unless this is already known `913` from the system designer. 

- `914` D. For Bridge Devices that comply with version 1.1+ of the I3C specification, the BCR for each `915` Virtual Target of a bridged endpoint will have Bit[4] set because the Virtual Target is a `916` Downstream Device that is being presented by the Bridge Device’s Peripheral logic. 

Copyright © 2021–2025 MIPI Alliance, Inc. **Public Release Edition** 

33 

I3C Application Note: Virtual Devices and Virtual Targets 

App Note Version 1.2 29-Aug-2025 

## `917` **6.2.3.2 Use of ENTDAA to Discover the Bridged Targets** 

- `918` Unlike the steps for configuring the bridged endpoints of a Bridge Device that is already known to the `919` Controller (i.e., one that knows about what it presents on the I3C Bus), the steps for configuring the bridged `920` endpoints of a Bridge Device that is detected during I3C Bus enumeration is quite different than the `921` SETBRGTGT CCC mechanism (see _**Section 6.2.3.1**_ above). In this case, the Controller does not need to `922` know anything about the Bridge Device or its bridged endpoints in advance. 

- `923` 

This mechanism works as follows: 

- `924` 1. The Bridge Device has some way to know what is connected to it, with some level of specificity. 

- `925` The Bridge Device might only know the bus format (e.g., I[2] C, SPI, UART, etc.) for each Target, or `926` it might know what type of device each Target is as well as other data about the specific endpoints. `927` The Bridge Device might know this configuration information from pin straps, from pin testing at `928` reset, from programmed fuses or NVMEM, or from some other means. 

- `929` _**Note:**_ 

- `930` _It is possible for the Controller to configure the Bridge Device in-band, via Private Write transfers._ `931` _The end result is the same: the Bridge Device receives its configuration regarding its bridged_ `932` _endpoints. This works similarly to the other specific methods, and so is not discussed separately_ `933` _here. The only notable aspect is that for the Controller to do this, the Bridge Device itself must_ `934` _have an assigned Dynamic Address, and the Controller must determine that the Bridge Device_ `935` _requires configuration data, before sending the configuration data via I3C Private Write transfers._ `936` _The Bridge Manager Function is responsible for receiving and applying this configuration data,_ `937` _before presenting the bridged endpoints as new Virtual Targets._ 

- `938` 2. During Dynamic Address Assignment with ENTDAA, the Bridge Device presents each bridged `939` Target as a separate and unique Virtual Target. 

- `940` This might happen during Bus Initialization, or it might happen later (i.e., after Bus Initialization `941` using a Hot-Join Request). 

- `942` • The Peripheral logic might reuse some or all of the Bridge Manager Function’s Manufacturer `943` ID, PID, BCR, and DCR. Alternately, the Peripheral logic might present these as entirely new `944` (or mostly new) values for each new Virtual Function. 

- `945` In either case, each new Virtual Function for a bridged endpoint must still appear to be `946` unique, for the Provisional ID and DCR values, across all other Targets within this Bridge `947` Device and the entire I3C Bus. 

- `948` 

   - The Controller will assign each such Virtual Target a unique Dynamic Address. 

- `949` • The Bridge Device’s Manager Function can also represent itself with a unique Provisional ID `950` and DCR if it needs or wants; this could also have been done in a previous round of assignment, `951` if the Controller programs it by private contract. 

- `952` • In general, the BCR values will describe the Bridge Device and bridging capabilities, per `953` _**[MIPI03]**_ at _**Section 4.3.1.2.1**_ . 

- `954` 

For example: 

- `955` • Each Virtual Target for a bridged endpoint will indicate a ‘limitation’ using BCR `956` Bit[0]. This will ensure that the Controller makes requests such as GETMXDS, `957` GETMWL and GETMRL, etc. 

- `958` • If a Virtual Target supports IBIs, then it will report this capability using BCR Bit[1]. `959` If IBI data payloads are also supported, then this shall be reported using BCR Bit[2]. 

- `960` • Each Virtual Target will also report support for other optional capabilities using the GETCAPS `961` CCC, including support for HDR Mode transfers (see _**[MIPI03]**_ at _**Section 4.3.7.3.19**_ ). 

Copyright © 2021–2025 MIPI Alliance, Inc. **Public Release Edition** 

34 

App Note Version 1.2 29-Aug-2025 

I3C Application Note: Virtual Devices and Virtual Targets 

`962` **6.2.4 Bridged Endpoints Exposed as Virtual Targets** `963` Each Downstream bridged endpoint exposed by the Bridge Device is also a _de facto_ Virtual Target which can `964` be treated as a normal I3C Target, though perhaps with some limitations required by bridging: 

- `965` 1. Virtual Targets for slower targets (such as I[2] C Devices) or endpoints on a slower external `966` Downstream interface will obviously need more time for write-read turnaround. 

- `967` This delay or turnaround time can typically be returned via the GETMXDS CCC. 

- `968` 2. Some Virtual Targets and/or the Bridge Device will have maximum write data limits. These can be `969` adjusted using the SETMWL and GETMWL CCCs, if supported. 

- `970` 3. The Bridge Device could NACK writes to a Downstream target if its buffers are full. 

- `971` 4. The Bridge Device could likely limit its support for advanced and optional features such as `972` transfers in HDR Modes, specialized CCCs, and other uses that might not translate well to `973` bridging. 

- `974` 5. For Bridge Devices that comply with version 1.1+ of the I3C specification, the Virtual Targets `975` presented by the Bridge Device need not support the GETCAPS Format 2 CCC with Defining `976` Byte VTCAPS. 

- `977` However, for some use cases, it might be advisable to include this support and present these `978` Virtual Targets as having Shared Peripheral logic (i.e., Virtual Target Type **3'd5** ). This could be `979` useful for Bridge Devices that indicate a Virtual Target Type **3'd2** for the Manager Function, since `980` the Controller might not otherwise have knowledge of which Virtual Targets are associated with `981` this Bridge Device. 

- `982` The method for determining which bridged endpoints on the Downstream bus or interface to expose is left `983` to the designer of the Bridge Device, and this could depend on the type of bus or interface that is being `984` bridged. In general there could be a 1-to-1 mapping for each Downstream target device to a particular `985` Dynamic Address, but the specifics will depend on the use case. 

- `986` _**Note:**_ 

- `987` _For certain use cases, the Virtual Target for a Downstream bridged endpoint might in fact be a_ `988` _virtualized function, or it might map to other resources that do not directly correspond with a unique_ `989` _device on the Downstream bus or interface, so the Dynamic Address could represent a notional entity_ `990` _or a composite endpoint._ 

## `991` **6.2.5 Bridged Devices and IBI** 

`992` The Bridge Device can use an IBI when a bridged endpoint sends a signal, such as pulling a GPIO of the `993` Bridge Device, to notify that it has new data (or, in the case of UART, that it has already sent new data). The `994` IBI could also be used for errors, such as a buffer overrun. The Controller and Target must have some `995` agreement on its use. 

`996` The Bridge Device could choose to support I3C Time Control, such as Asynchronous Time Control, which `997` would allow the Bridge Device to record the time when the GPIO was pulled (or when data was written to `998` the UART) in order to provide that timestamp data to the Controller. 

`999` The Bridge Device could first read data from the Target on GPIO assert (i.e., before the IBI is generated), or it could simply wait for the Controller to request the data. 

- `1000` 

`1001` If IBIs are used, then the Bridge Device might opt to pre-emptively read the new data from a bridged `1002` endpoint, store the data in an internal buffer, and then signal the Upstream Controller with the IBI. The Bridge `1003` Device might also choose to support Pending Read Notifications (see _**[MIPI03]**_ at _**Section 4.3.6.2.2**_ ) when `1004` signaling the presence of newly-buffered data from a bridged endpoint. 

Copyright © 2021–2025 MIPI Alliance, Inc. **Public Release Edition** 

35 

I3C Application Note: Virtual Devices and Virtual Targets 

App Note Version 1.2 29-Aug-2025 

## `1005` **6.3 Routing Devices** 

`1006` The MIPI I3C Specification _**[MIPI03]**_ also defines simple CCC support for I3C routing, to enable Routing `1007` Devices that can store and forward Private Write/Read transactions from a main I3C Bus Segment to I3C `1008` Target Devices on one or more Downstream I3C Bus Segments. All such segments have independent `1009` parameters and different sets of Dynamic Addresses, but still enable communication via the Routing Device. 

## `1010` **6.3.1 Architectural Overview** 

`1011` A Routing Device shares some key features and capabilities of a Composite I3C Device (see `1012` _**Section 5.2.1**_ above) that uses Peripheral logic to present its Virtual Targets, and that interacts with its `1013` Upstream I3C Bus through its additional capabilities (i.e., capabilities over and above those required of a `1014` Simple I3C Target). 

`1015` _**Figure 8**_ shows an example of an I3C Routing Device that presents multiple I3C Virtual Targets on an I3C `1016` Bus, where each Virtual Target is a Routing Target Function that provides a Read/Write interface to its `1017` corresponding Downstream I3C Bus Segment. Each Routing Target Function has an assigned Dynamic `1018` Address that serves as the access point for interfacing with a set of Transfer Queues. The Transfer Queues `1019` are accessed by a dedicated I3C Bus Controller for the Downstream I3C Bus Segment, which drives the `1020` Private Write/Read transactions to the indicated I3C Target Devices on its segment. In this example, the I3C `1021` Routing Device also has a Routing Manager function (per _**Section 6.1.1**_ above) as the primary Virtual Target, `1022` used by the I3C Controller on its Upstream I3C Bus Segment to configure and manage the Routing Device `1023` and its presentation of the Downstream I3C Bus Segments. 

**==> picture [417 x 275] intentionally omitted <==**

**----- Start of picture text -----**<br>
SDA<br>I3C<br>PRIMARY<br>CONTROLLER SCL<br>ACTIVE<br>PWR I3C<br>GND TARGET<br>I/O PERIPHERAL<br>I3C Bus<br>EP I/O<br>Controller<br>Downstream Bus<br>... Routing Target  Segment #1<br>Function #1 Xfer<br>Queues<br>Downstream Bus<br>Segment #2<br>HL mt<br>Routing  I3C Bus<br>Routing Target  EP I/O<br>Function #2 Manager  Controller<br>Function<br>I3C<br>or TARGET<br>S56 I3C ROUTING DEVICE<br>(with Peripheral Logic and Downstream Buses)<br>LEGEND<br>I3C CONTROLLER I3C ROUTING  I3C TARGET  I3C TARGET<br>(Primary) DEVICE (Virtual) (Downstream)<br>**----- End of picture text -----**<br>


`1024` 

**Figure 8 I3C Routing Device with Downstream I3C Buses as Virtual Targets** 

Copyright © 2021–2025 MIPI Alliance, Inc. 

36 

**Public Release Edition** 

App Note Version 1.2 29-Aug-2025 

I3C Application Note: Virtual Devices and Virtual Targets 

## `1025` **6.3.2 Routing Manager Function** 

`1026` In general, Routing Devices present at least one Routing Manager Function as a Virtual Target. A Routing `1027` Manager Function exposes the Device’s presence on the I3C Bus (i.e., the Upstream segment) and describes `1028` its capabilities and optional features (see _**Section 6.1.1**_ above). 

`1029` If such Devices are fully compliant with version 1.1+ of the I3C Specification _**[MIPI03]**_ , then they must `1030` report this capability in the Bus Configuration Register. Specifically, the Manager Function’s BCR Bit[4] `1031` must indicate that that it is a Virtual Target (see _**[MIPI03]**_ at _**Section 4.3.1.2.1**_ ). Such Targets will also support `1032` the GETCAPS CCC Format 2 CCC with Defining Byte VTCAPS (see _**Section 4.3.7.3.19**_ ) to describe more `1033` details regarding the Routing Device’s capabilities and features. 

- `1034` • Manager Functions for Routing Devices will support the GETCAPS Format 2 CCC with Defining `1035` Byte VTCAPS and return a message of at least one byte, but preferably two bytes (i.e., both the `1036` VTCAP1 byte and the VTCAP2 byte). 

- `1037` • In the first byte (VTCAP1), Bits[2:0] will have a value of **3'd3** to inform the I3C Controller that `1038` it must use the SETROUTE CCC to configure the Routing Device and its Routes to `1039` Downstream I3C Bus Segments. 

- `1040` • It is recommended that the Manager Function have a different value for its Device `1041` Characteristics Register (DCR) than the DCR of its Routing Target Function(s). 

- `1042` • Bit[5] will be set to **1'b1** to indicate that this Device also supports the Virtual Target Detect `1043` operation using the RSTACT CCC, as specified in the I3C Specification at _**Section 4.3.7.3.23**_ . `1044` Support for this operation is recommended for Manager Functions of all Routing Devices. 

- `1045` • In the second byte (VTCAP2), the field values will reflect the Routing Device’s implementation `1046` and its configuration of Downstream I3C Bus Segments. 

- `1047` • Bit[2] will have a value of **1'b1** , unless the Routing Device only has a single Downstream I3C `1048` Bus Segment and allows its Downstream Target Devices to have the same Dynamic `1049` Addresses as the ones the I3C Controller on the Upstream I3C Bus Segment assigned. Special `1050` restrictions might apply for such a use case, and therefore Bit[2] would have a value of **1'b0** . 

- `1051` • Bits[4:3] can be set at the implementer’s discretion, and will reflect the Routing Device’s `1052` capabilities including whether it is capable of caching context and event enable/disable `1053` configuration (such as SETBUSCON, ENEC, or DISEC) that the I3C Controller on the `1054` Upstream I3C Bus Segment previously Broadcast. 

Copyright © 2021–2025 MIPI Alliance, Inc. **Public Release Edition** 

37 

I3C Application Note: Virtual Devices and Virtual Targets 

App Note Version 1.2 29-Aug-2025 

## `1055` **6.3.3 Downstream Bus Target Presentation** 

`1056` A Downstream I3C Bus Segment exposed by a Routing Device will present itself as a Virtual Target Device, `1057` with BCR Bit[4] indicating that it is also a Virtual Target. 

- `1058` For Routing Devices that support one or more Routes to Downstream I3C Bus Segments, each such Route is `1059` a target, is presented as a Virtual Target Device, and is known as a Routing Target Function. 

- `1060` • Target Functions for Routing Devices will support the GETCAPS Format 2 CCC with Defining `1061` Byte VTCAPS (see _**[MIPI03]**_ at _**Section 4.3.7.3.19**_ ) and return a message of at least one byte, but `1062` preferably two bytes (i.e., both the VTCAP1 byte and the VTCAP2 byte). 

- `1063` • In the first byte (VTCAP1), Bits[2:0] will have a value of **3'd3** to inform the I3C Controller that `1064` the Routing Target Function represents a Route to a Downstream I3C Bus Segment, and that it `1065` must be configured using its Manager Function (see _**Section 6.3.2**_ above). 

- `1066` • It is recommended that the Routing Target Function DCR value be different from the Manager `1067` Function DCR value. 

- `1068` • Bit[5] will be set to **1'b1** to indicate that this Device also supports the Virtual Target Detect `1069` operation using the RSTACT CCC, as specified in the I3C Specification at _**Section 4.3.7.3.23**_ . `1070` Support for this operation is recommended for Target Functions of all Routing Devices. 

- `1071` • In the second byte (VTCAP2), the fields will have values applicable to the Downstream I3C `1072` Bus Segment being presented: 

- `1073` • Bits[1:0] would have a value of **2'd1** , unless special exceptions apply, as per the use case. 

- `1074` • Bit[2] will have a value of **1'b1** to indicate that this Target Function will hide the addresses of `1075` its I3C Target Device(s) on this Downstream I3C Bus Segment, and will transparently remap `1076` all commands and private writes/reads based on the message contents. 

- `1077` • Bits[4:3] will return a value of **2'd0** . It is expected that all Target Functions exposed by a `1078` given Routing Device would share the same settings for Bus Context and Conditions (which `1079` are reported via the Manager Function). 

`1080` Routing Devices might also allow the Downstream Bus Segments, or the I3C Targets on such segments, to `1081` be indirectly configured by the I3C Controller on the Upstream Bus segment via each Routing Target `1082` Function, per _**Section 6.1.2**_ above. However, the Bus Controller of the Downstream Bus segment is `1083` responsible for assigning individual Dynamic Addresses to each of the I3C Targets on that segment. If the `1084` Routing Device serves this function, then it will typically configure each Downstream Bus segment and `1085` serves as the segment’s Active Controller (as well as the Primary Controller for initialization). 

Copyright © 2021–2025 MIPI Alliance, Inc. **Public Release Edition** 

38 

App Note Version 1.2 

I3C Application Note: Virtual Devices and Virtual Targets 

29-Aug-2025 

## `1086` **6.3.3.1 Encapsulated Transactions to Downstream Bus** 

`1087` Typical Routing Devices do not directly map the I3C Targets on their Downstream Bus segment(s) to the `1088` Upstream Bus segment, meaning that the Primary Controller on the Upstream Bus segment must `1089` communicate via the Routing Target Function in order to drive I3C transactions on the Downstream Bus `1090` segment. This requires some encapsulation of the I3C transactions that are sent over the Upstream Bus `1091` segment, as part of the Routing Target Function’s I3C content protocol. 

`1092` Once a Routing Device has been configured and a Route to a Downstream Bus segment has been established, `1093` the Routing Target Function receives Private Writes from its Upstream Bus (i.e., from the Primary `1094` Controller). The Routing Device then examines the encapsulated write data per the I3C content protocol, `1095` enqueues the I3C transfer commands based on the data structures that it received, and then its internal Bus `1096` Controller executes the I3C transfer commands on the Downstream Bus segment. Similarly, the Routing `1097` Device collects the results of each I3C transfer command, enqueues them for delivery to the Upstream Bus `1098` segment, and then notifies the Primary Controller that its requested transactions have been processed (i.e., `1099` executed either to successful completion, failure, or termination for other reasons) per the I3C content `1100` protocol of the Routing Target Function. 

`1101` The Routing Device could also relay any In-Band Interrupts (IBIs) sent by I3C Targets on the Downstream `1102` Bus segment to the Upstream Bus segment, so that the Primary Controller could be aware of them. This could `1103` happen in one of two different ways: 

- `1104` • The Primary Controller could periodically poll the Routing Device’s Routing Target Function to `1105` see whether any transfer command responses or IBI Notifications are pending (i.e., via a Private `1106` Read). If any IBI Notifications are pending, then the Routing Target Function provides ACK and `1107` then returns a description of transfer command responses and/or IBI Notifications (i.e., per the I3C `1108` content protocol). 

- `1109` • The Routing Device could raise an IBI Request on the Upstream Bus segment containing a short `1110` notification that some transfer command responses or IBI Notifications are pending and must be `1111` read (e.g., using the I3C Pending Read Notification contract, per _**[MIPI03]**_ at _**Section 4.3.6.2.2**_ ). `1112` The subsequent read contains a description of transfer command responses and/or IBI `1113` Notifications (i.e., per the I3C content protocol). 

`1114` Notification of such responses and/or IBIs could be encapsulated as part of the I3C content protocol for a `1115` Routing Target Function. For IBI Notifications, this encapsulation would include status, such as whether the `1116` Bus Controller provided ACK or NACK to each IBI Request from a Downstream I3C Target, identified by `1117` its Dynamic Address, as well as whether the IBI Request was ACK’d. If the IBI Request was ACK’d, then `1118` the encapsulation would also include any IBI data payload (if applicable) as well any subsequent read that `1119` would be performed automatically by the Bus Controller (i.e., for an IBI that signaled a Pending Read `1120` Notification, per _**[MIPI03]**_ at _**Section 4.3.6.2.2**_ ). 

`1121` _**Note:**_ 

`1122` _The specific I3C content protocol that a Routing Target Function supports, for encapsulated I3C_ `1123` _transfer commands and responses as well as IBI notifications, is not defined in this Application Note,_ `1124` _nor is it defined in the I3C Specification._ 

Copyright © 2021–2025 MIPI Alliance, Inc. **Public Release Edition** 

39 

I3C Application Note: Virtual Devices and Virtual Targets 

App Note Version 1.2 29-Aug-2025 

## `1125` **6.3.3.2 Downstream Target Mapping Option** 

`1126` For Routing Devices that only support one Route to a Downstream I3C Bus Segment, an implementer could `1127` decide to present some or all of the I3C Target Devices on the Downstream I3C Bus Segment as a Virtual `1128` Target Device that can be directly addressed (i.e., via store-and-forward) on the Upstream Bus segment. For `1129` some use cases, this removes the need to encapsulate certain I3C transactions involving the Downstream I3C `1130` Target. 

`1131` If this option is chosen, then each such Target Device would have its own Dynamic Address that is visible on `1132` the Upstream Bus segment (i.e., assigned directly by the Primary Controller), for which the Routing Device’s `1133` Peripheral logic must act as a proxy or intermediary. 

`1134` Each mapped Downstream Target could either be configured automatically by the Routing Device (i.e., as `1135` and when it is discovered by the Bus Controller), or via other configuration commands that could be sent `1136` from the Primary Controller. As each mapped Downstream Target is configured (i.e., virtually exposed) to `1137` the Upstream Bus segment, the Routing Device simulates a Hot-Join Request for a new Virtual Target and `1138` allows the Primary Controller to assign a Dynamic Address that is used for that particular mapping. The `1139` Routing Device then associates that new Dynamic Address with the mapped Downstream Target for future `1140` communications (e.g., Private Writes, Private Reads, CCCs). 

- `1141` 

## _**Note:**_ 

`1142` _The Routing Device would need to intercept certain CCCs such as SETNEWDA from being sent to_ `1143` _the mapped Downstream Target, as the Dynamic Address assigned by the Primary Controller only_ `1144` _applies to communications with the Virtual Target (i.e., as presented to the Upstream Bus segment)._ 

`1145` As the Primary Controller sends I3C transactions to the Virtual Target, the Routing Device’s Peripheral logic `1146` would respond on behalf of the Downstream Target, in a manner similar to a composite I3C Device (per `1147` _**Section 5.2**_ ) per the transaction type: 

- `1148` • **For Write transactions:** The Routing Device would typically ACK the write on behalf of the `1149` Downstream I3C Target, then cache the data for later relaying to the Downstream I3C Bus. 

- `1150` • **For Read transactions:** The Routing Device must only ACK if it has data ready to respond (i.e., `1151` from a pre-emptive read that it could have issued earlier, or some other notification from the `1152` Downstream Target); otherwise, it must NACK the read. 

- `1153` • **For Direct CCCs:** The Routing Device typically responds to Direct CCCs sent to the Downstream `1154` Target. It could optionally pre-fetch certain responses (i.e., for Direct GET or Direct Read) based `1155` on known status or a private contract, per the Downstream Target type. This use model does not `1156` work well for all Direct CCCs. 

`1157` _**Figure 9**_ shows an example of an I3C Routing Device (derived from _**Figure 8**_ ) that also maps two I3C `1158` Targets on its Downstream I3C Bus segment as separate Virtual Targets, presented via its Peripheral logic. `1159` The Routing Device could still accept I3C Bus transactions directed to the entire Bus via its Routing Target `1160` Function (i.e., either Broadcast CCCs or transactions directed to any other I3C Targets that might not be `1161` mapped to the Upstream Bus segment). 

Copyright © 2021–2025 MIPI Alliance, Inc. **Public Release Edition** 

40 

I3C Application Note: Virtual Devices and Virtual Targets 

**==> picture [459 x 459] intentionally omitted <==**

**----- Start of picture text -----**<br>
App Note Version 1.2  I3C Application Note: Virtual Devices and Virtual Targets<br>29-Aug-2025<br>SDA<br>I3C<br>PRIMARY<br>CONTROLLER SCL<br>ACTIVE Downstream Bus<br>Segment #1<br>PWR I3C<br>GND TARGET  A<br>I/O PERIPHERAL<br>I3C Bus<br>EP I/O<br>Controller<br>Routing Target  I3C<br>Function #1 Xfer TARGET  B<br>Queues<br>Mapped  Mapped  Routing<br>Target  Target<br>Function for  A  Function for  B  FunctionManager  Error Handling<br>I3C ROUTING DEVICE<br>(with Peripheral Logic and Downstream Buses)<br>LEGEND<br>I3C CONTROLLER I3C ROUTING  I3C TARGET  I3C TARGET<br>(Primary) DEVICE (Virtual) (Downstream)<br>1162<br>1163  Figure 9 I3C Routing Device with Mapped Downstream Targets<br>1164  Note:<br>1165  The decision to map Downstream Targets to the Upstream I3C Bus segment is left up to the<br>1166  implementer, as it requires an additional level of routing complexity that might not be appropriate for<br>1167  all implementations or all use cases. If this option is chosen, then the Routing Device would present<br>1168  a Virtual Target for each such mapped Downstream Target as though it had “Shared Peripheral Logic”<br>1169  (i.e., had Virtual Target type  3'd5 ). Additionally, in this scenario, an implementer must still configure<br>1170  the Routing Device to present the Route as a Target Function for transactions directed to the<br>1171  Downstream Bus segment, or to any other such I3C Targets that do not map to Virtual Targets that<br>1172  [Se] can be directly addressed on the Upstream Bus segment.<br>**----- End of picture text -----**<br>


Copyright © 2021–2025 MIPI Alliance, Inc. **Public Release Edition** 

41 

I3C Application Note: Virtual Devices and Virtual Targets 

App Note Version 1.2 29-Aug-2025 

`1173` **6.3.4 Support for Remote Downstream Buses** 

`1174` Typical I3C Routing Devices are implemented as single-component solutions. However, an advanced I3C `1175` Routing solution could also extend the I3C Routing solution into two distinct components, using a higher- `1176` speed link or network between them. 

`1177` 

The two components are envisioned as follows: 

- `1178` • **An advanced I3C Routing Device** (i.e., the upper portion) that connects to the Upstream I3C Bus `1179` segment, presents Virtual Targets on this segment, manages the transactions to/from its Primary `1180` Controller, and connects to a higher-speed link; and 

- `1181` • **A remote Endpoint** (i.e., the lower portion) that also connects to that same link, owns the `1182` Downstream I3C Bus segment (i.e., contains the I3C Bus Controller for this segment), and drives `1183` the enqueued Private Write/Read transactions to the indicated I3C Target Devices on its segment. 

**==> picture [473 x 448] intentionally omitted <==**

**----- Start of picture text -----**<br>
1184  Figure 10  shows an example of a two-component I3C Routing solution featuring an I3C Routing Device<br>1185  (derived from  Figure 8 ) paired with a remote Endpoint, connected via a higher-speed link. The remote<br>1186  Endpoint controls its Downstream I3C Bus segment and receives transactions from the I3C Routing Device.<br>SDA<br>I3C<br>PRIMARY<br>CONTROLLER SCL<br>ACTIVE<br>PWR I3C<br>GND TARGET<br>a I/O PERIPHERAL e I3C Bus<br>EP Controller I/O<br>Downstream Bus<br>... Routing Target  Segment #1<br>Function #1 Xfer<br>(Local) Queues<br>Routing Target  Routing<br>Function #2 Manager  Session<br>(Remote) Function Management<br>Remote Link<br>to Downstream<br>I3C ROUTING DEVICE<br>(with Peripheral Logic and Local Downstream Bus)<br>Link from<br>Upstream Link State and<br>Session<br>Management<br>Queues<br>Downstream Bus<br>Segment #2<br>I3C Bus<br>EP Controller I/O<br>I3C<br>I3C REMOTE ENDPOINT TARGET<br>(with Remote Downstream Bus)<br>LEGEND<br>I3C CONTROLLER I3C ROUTING  I3C TARGET  I3C TARGET<br>(Primary) DEVICE (Virtual) (Downstream)<br>**----- End of picture text -----**<br>


**Figure 10 I3C Routing Device with Remote Link to Downstream Bus** 

`1187` 

Copyright © 2021–2025 MIPI Alliance, Inc. **Public Release Edition** 

42 

App Note Version 1.2 29-Aug-2025 

I3C Application Note: Virtual Devices and Virtual Targets 

## `1188` _**Note:**_ 

`1189` _In the example above, the Virtual Target for Routing Target Function #1 is still associated with a_ _**local**_ `1190` _Downstream I3C Bus Segment, whereas the Virtual Target for Routing Target Function #2 is now_ `1191` _associated with a_ _**remote** Downstream I3C Bus Segment, provided by the routed Endpoint device._ `1192` _The key architectural difference from_ **Figure 8** _is the insertion of a remote link in the Transfer Queues_ `1193` _of the I3C Routing Device. In effect, the remote link extends the Transfer Queues across a longer_ `1194` _physical distance, which could slightly increase the latency of I3C Private Write/Read transfers that_ `1195` _are enqueued by the Primary Controller on the Upstream I3C Bus Segment. However, the overall_ `1196` _flow remains similar to a single-component I3C Routing solution._ 

`1197` It is beyond the scope of this Application Note to detail the complete set of requirements or implementation `1198` details pertaining to the higher-speed link between such an I3C Routing Device and any connected remote `1199` Endpoint devices that control the Downstream I3C Bus segments. However, implementers should consider `1200` some minimal guidelines and expectations for such a solution: `1201` • The high-speed link or network between the Routing Device and the remote Endpoint must `1202` provide high reliability and robustness for transmitting messages or packets for enqueued I3C `1203` transfer commands, I3C IBI Notifications or other messages between these components. `1204` • Nonetheless, if the high-speed link or network is interrupted or if an established connection `1205` fails, then the I3C Routing Device must notify the Primary Controller, and not accept new `1206` enqueued I3C transfer commands directed to the Downstream I3C Bus segment. 

- `1207` • The high-speed link or network must also be bi-directional in nature, and have sufficiently high `1208` bandwidth and low latency, in order to mitigate the performance impacts on a remote I3C Routing `1209` solution (as compared with a single-component I3C Routing Device). 

- `1210` • The method for sending packets or messages over this link or network must allow both I3C `1211` transfer commands and IBI notifications (i.e., the encapsulated I3C content protocol for the I3C `1212` Routing Target Function) as well as link management commands and responses, which might be `1213` specific to the type of high-speed link or network. 

- `1214` • The remote Endpoint could either expose its own Transfer Queue size or provide some method of `1215` flow control to the Routing Device, in order to inform it of any limits that it might have. 

- `1216` • The I3C Bus Controller in the remote Endpoint must be sufficiently autonomous, in order to `1217` handle conditions (such as IBIs raised by Downstream I3C Targets) without requiring immediate `1218` response from the logic inside the Routing Device. 

- `1219` • The I3C content protocol for each Routing Target Function that is linked to a remote Downstream `1220` Bus segment could be the same as an I3C content protocol for a Routing Target Function of a `1221` single-component I3C Routing Device (see _**Section 6.3.3.1**_ above) for consistency and `1222` interoperability. `1223` • If the high-speed link or network supports a “one-to-many” connection scheme (i.e., where an I3C `1224` Routing Device could establish connections to multiple remote Endpoints) then the Routing `1225` Device could present each of its connected Endpoints as a unique Virtual Target (i.e., one for each `1226` Downstream Bus segment). 

- `1227` • As each Endpoint is connected, the Peripheral Logic simulates a Hot-Join Request on the `1228` Upstream I3C Bus segment, presenting a new Virtual Target to the Primary Controller, where `1229` each receives a unique Dynamic Address. 

- `1230` • The Routing Device then steers the encapsulated I3C transfer commands (i.e., Private `1231` Writes/Reads) to each remote Endpoint’s Downstream I3C Bus segment, based on the Dynamic `1232` Address. 

- `1233` • The Routing Manager Function inside the Routing Device could offer additional session `1234` management capabilities to the Primary Controller of the Upstream I3C Bus segment. These might `1235` be specific to the type of high-speed link or network. Alternately, the session management `1236` capabilities of the Routing Device could be pre-configured, or configured via other means (i.e., out `1237` of band). 

Copyright © 2021–2025 MIPI Alliance, Inc. 

43 

**Public Release Edition** 

I3C Application Note: Virtual Devices and Virtual Targets 

App Note Version 1.2 29-Aug-2025 

## `1238` **6.3.5 Support for Controller Role or Segment Secondary Controller** 

`1239` A Routing Device could also offer Secondary Controller capabilities on any of its Downstream I3C Bus `1240` Segments. For such a Routing Device, its I3C Bus Controller logic for the Downstream segment must have `1241` Secondary Controller capabilities, and could optionally initialize as a Secondary Controller, if so configured. 

`1242` If such a Routing Device is capable of initializing as either the Primary Controller of the Downstream `1243` segment or as a Secondary Controller of it, then the Routing Device must be configured to provide a suitable `1244` Primary Controller (i.e., one with a separate I3C Device) on that Downstream segment, and the Routing `1245` Device must contain logic to manage the Controller Role Handoff procedure with respect to its Routing `1246` Target Function. Additionally, the Routing Device must be capable of handling the case in which it initializes `1247` as the Primary Controller of that Downstream segment, but then subsequently passes the Controller Role to `1248` another Controller-capable Device (i.e., one that initialized as a Secondary Controller and is capable of taking `1249` the Controller Role). 

`1250` In either case, the Routing Device must know when it is not the Active Controller, since it cannot route Private `1251` Write/Read transfers from its Transfer Queues (i.e., to/from the Upstream segment) until it receives the `1252` Controller Role and can drive enqueued transfers on the Downstream segment. The Routing Target Function `1253` could implement support for sending an IBI to the Upstream segment to notify the Active Controller when it `1254` has handed the Controller Role off (i.e., is no longer the Active Controller of the Downstream segment). 

`1255` _**Note:**_ 

`1256` _If the Routing Device manages multiple Downstream segments and has the Secondary Controller_ `1257` _capability for some or all of these segments, then it must separately manage the initial Role_ `1258` _configuration and subsequent Controller Role transitions for each of these segments._ 

`1259` _**Figure 11**_ shows a partial view of an example Routing Device (derived from a portion of _**Figure 8**_ ) with one `1260` such Downstream I3C Bus Segment, where the I3C Bus Controller logic has Secondary Controller capability. `1261` For this Downstream segment the Routing Device can serve as both Active Controller and Secondary `1262` Controller, and can manage the transition between the Controller and Target roles on its I3C Bus Segment. `1263` The Transfer Queues that serve this I3C Bus Segment could (optionally) be bi-directional to support limited `1264` transactions in I3C Target mode. In this example, the Routing Device has been configured to act as a `1265` Secondary Controller for this I3C Bus Segment on initialization, since there is also a Primary Controller on `1266` the same segment (which is currently the Active Controller). 

**==> picture [226 x 182] intentionally omitted <==**

**----- Start of picture text -----**<br>
To Upstream<br>Segment<br>PERIPHERAL<br>Controller Role<br>Request &<br>Handoff FSM<br>Xfer<br>Queues<br>Downstream Bus<br>I3C SECONDARY CONTROLLER<br>Segment<br>EP I3C BUS I3C I/O<br>CONTROLLER TARGET<br>(not active) (active)<br>I3C<br>TARGET I3C<br>CONTROLLER<br>ACTIVE<br>**----- End of picture text -----**<br>


**Figure 11 I3C Routing Device with Downstream Secondary Controller Capability** 

`1267` 

Copyright © 2021–2025 MIPI Alliance, Inc. **Public Release Edition** 

44 

App Note Version 1.2 29-Aug-2025 

I3C Application Note: Virtual Devices and Virtual Targets 

`1268` _**Note:**_ `1269` _The example shown in_ _**Figure 11** does not imply that the Controller-capable Device on the_ `1270` _Downstream Bus segment has any effective control or influence over the Upstream Bus segment._ `1271` _The Transfer Queues and other routing-specific logic inside the Routing Device will manage all_ `1272` _communications across the Bus segments, and the Routing Device will present itself appropriately_ `1273` _to each Bus segment (i.e., with its proper Role). In this example, the Upstream Bus segment is not_ `1274` _visible to the Downstream Bus segment._ 

Copyright © 2021–2025 MIPI Alliance, Inc. 

45 

**Public Release Edition** 

I3C Application Note: Virtual Devices and Virtual Targets 

App Note Version 1.2 29-Aug-2025 

## `1275` **6.4 Hub Devices** 

`1276` Specialized I3C Hub Devices can provide isolation between the separate electrical domains of an Upstream `1277` Bus segment and a Downstream Bus segment, enabling use cases where the two segments have electrical `1278` property differences (even incompatibilities) that necessitate such isolation. 

`1279` For example, the I3C Target Devices in a Downstream Bus segment might operate at different electrical `1280` parameters, from the Upstream segment, including but not limited to: 

- `1281` • Different operating voltage requirements (i.e., parameter **VDD** , per _**[MIPI03]**_ at _**Section 4.3.11.1**_ ) 

- `1282` • Different current requirements (i.e., parameter **Ii** , per _**[MIPI03]**_ at _**Section 4.3.11.1**_ ) 

`1283` An I3C Hub Device can also provide buffering to alleviate the total loading of the I3C Bus, enabling `1284` applications in which the total number of I3C Target Devices would result in excessively high capacitance `1285` (i.e., parameters **Ci** and **Cb** ) if all the Devices were resident on the same Bus segment. 

- `1286` It is beyond the scope of this Application Note to detail the complete set of capabilities that could theoretically `1287` be provided by such an I3C Hub Device, but the core Hub Device concepts can be stated as: 

- `1288` • Isolation between the Upstream and Downstream Bus segments; 

- `1289` • Configurable I/O parameters for the Downstream Bus segment; and 

- `1290` • At least one Virtual Target, presented by the I3C Hub Device as a Hub Manager Function, that `1291` provides the I3C Controller on the Upstream segment control over those configurable parameters. `1292` (I.e., via CCCs or Private Write/Read transactions to the Hub Manager Function’s Dynamic `1293` Address.) 

`1294` _**Note:**_ 

`1295` _In a strict sense, simple I3C Hub Devices that provide isolation between Upstream and Downstream_ `1296` _I3C Bus Segments might not have a Virtual Target that acts as a Hub Manager Function, if the_ `1297` _configuration of the Hub Device is accomplished by other means (i.e., not using in-band transactions_ `1298` _on the Upstream Bus segment from the I3C Controller). However, this Application Note assumes that_ `1299` _the advanced capabilities and configurability of such Hub Devices will be a desirable feature, and_ `1300` _that the Virtual Target capabilities defined in this Application Note will provide a mechanism for_ `1301` _providing this feature. In the remaining sections of this Application Note, the term ‘Hub Device’ is_ `1302` _interpreted as an advanced I3C Hub Device that includes this capability, presents a Virtual Target as_ `1303` _a Hub Manager Function, and allows configuration via this Virtual Target._ 

Copyright © 2021–2025 MIPI Alliance, Inc. **Public Release Edition** 

46 

App Note Version 1.2 29-Aug-2025 

I3C Application Note: Virtual Devices and Virtual Targets 

## `1304` **6.4.1 Architectural Overview** 

`1305` An I3C Hub Device is similar in concept to a Composite I3C Device (see _**Section 5.2.1**_ above) that uses `1306` Peripheral logic to present at least one Virtual Target, and that interacts with its Upstream I3C Bus through `1307` its additional capabilities (i.e., capabilities over and above those required of a simple I3C Target). If the Hub `1308` Device also presents other Virtual Targets (i.e., ones not shown below, or not described in this Application `1309` Note), then the Peripheral Logic could have additional capabilities, however these are not required. 

`1310` The Hub Device also contains Isolation Logic that enables I3C transactions to flow across the boundary `1311` between the electrically isolated segments, using appropriate isolation methods. This isolation could be `1312` accomplished by specialized circuits that track the states of the SDA and SCL lines, repeating or mirroring `1313` actions taken on one segment and replicating them to the other segment, per the I3C Specification (see `1314` _**Section 6.4.3**_ below). 

`1315` _**Figure 12**_ shows an example of a Hub Device that presents a single I3C Virtual Target on an I3C Bus, namely `1316` a Hub Manager Function. A Hub Manager Function is used by the Upstream Bus segment’s I3C Controller `1317` to configure and manage the Hub Device and the electrical I/O parameters of its Downstream Bus segment, `1318` as well as to control the Isolation Logic’s operating mode. 

```
1319
```

**==> picture [338 x 225] intentionally omitted <==**

**----- Start of picture text -----**<br>
SDA<br>I3C<br>PRIMARY<br>CONTROLLER SCL<br>ACTIVE<br>PWR<br>GND<br>I/O PERIPHERAL<br>I3C<br>TARGET<br>Hub Manager  Isolation I/O<br>Function Logic<br>Isolated Segment<br>I3C HUB DEVICE<br>(with Isolation Logic)<br>LEGEND<br>I3C CONTROLLER I3C HUB  I3C TARGET  I3C TARGET<br>(Primary) DEVICE (Virtual) (Downstream)<br>**----- End of picture text -----**<br>


**Figure 12 I3C Hub Device with Isolation Logic and Downstream Target Devices** 

`1320` The Peripheral logic in such a Hub Device maintains the Dynamic Address of the Virtual Targets, including `1321` the Hub Manager Function (and potentially other optional Functions), and also responds to I3C transactions `1322` that address such Virtual Targets. However, the Peripheral logic allows I3C transactions that address other `1323` Target Addresses (i.e., those not assigned to any internal Virtual Targets) to pass to the Isolation Logic where `1324` they can be tracked and echoed to the Downstream Bus segment. 

Copyright © 2021–2025 MIPI Alliance, Inc. **Public Release Edition** 

47 

I3C Application Note: Virtual Devices and Virtual Targets 

App Note Version 1.2 29-Aug-2025 

## `1325` **6.4.2 Hub Manager Function** 

- `1326` Hub Devices present at least one Hub Manager Function as a Virtual Target. A Hub Manager Function `1327` exposes the Device’s presence on the I3C Bus and describes its capabilities and optional features (see `1328` _**Section 6.1.1**_ above). 

- `1329` If such Devices are fully compliant with version 1.1+ of the I3C Specification _**[MIPI03]**_ , then they must `1330` report this capability in the Bus Configuration Register (BCR) for the Manager Function’s Virtual Target. `1331` Specifically, the Manager Function’s BCR Bit[4] must indicate that that it is a Virtual Target (see _**[MIPI03]**_ `1332` at _**Section 4.3.1.2.1**_ ). Such Targets will also support the GETCAPS CCC Format 2 CCC with Defining Byte `1333` VTCAPS (see _**[MIPI03]**_ at _**Section 4.3.7.3.19**_ ) to describe more details regarding the Hub Device’s `1334` capabilities and features. 

- `1335` • Manager Functions for Hub Devices will support the GETCAPS Format 2 CCC with Defining `1336` Byte VTCAPS and return a message of at least one byte (i.e., the VTCAP1 byte). 

- `1337` • In the first byte (VTCAP1), Bits[2:0] will have the value **3'd6** to indicate that it is a Hub Device `1338` that supports pass-through transactions. 

- `1339` • The second byte (VTCAP2) does not currently define any bit fields relating to Hub Device `1340` capabilities or features. 

- `1341` The Hub Manager Function typically also describes its capabilities and optional features, including: 

- `1342` • The type of Isolation Logic, including the electrical parameters and I/O pad controls that the I3C `1343` Controller can access or change; 

- `1344` • Any additional internal routing delays that the Isolation Logic might add (i.e., for each transaction `1345` that goes through the Isolation Logic to the I/O pads and addresses an I3C Target Device on the `1346` Downstream segment); 

- `1347` • The Isolation Logic’s initial mode (i.e., whether it is engaged vs. disengaged) when the Hub `1348` Device is powered on and initialized by the I3C Controller; 

- `1349` • The method of engaging the Isolation Logic and bringing any I3C Target Devices on its `1350` Downstream Bus segment online (i.e., with a virtual connection to the Upstream Bus segment); `1351` and 

- `1352` • Any additional advanced capabilities that might be supported, including error handling `1353` capabilities. 

- `1354` _**Note:**_ 

`1355` _The specific I3C content protocol that a Hub Manager Function supports is not defined in this_ `1356` _Application Note, nor is it defined in the I3C Specification._ 

Copyright © 2021–2025 MIPI Alliance, Inc. **Public Release Edition** 

48 

App Note Version 1.2 29-Aug-2025 

I3C Application Note: Virtual Devices and Virtual Targets 

## `1357` **6.4.3 Isolation Logic and Transactions for Downstream Devices** 

`1358` The Isolation Logic plays a special role in tracking the actions that are initiated by I3C Devices on the `1359` Upstream Bus segment and repeating or mirroring such actions, so that they might be repeated (or replicated) `1360` to the Downstream Bus segment. Similarly, the Isolation Logic must track actions that the I3C Devices on `1361` the Downstream Bus segment might initiate, and must track these in order to repeat them to the Upstream `1362` Bus segment. 

`1363` Notably, the Isolation Logic must contain a Leader/Follower tracking circuit that identifies electrical state `1364` changes on one Bus segment and replicates them to the other segment with minimal delay. This tracking `1365` circuit must determine which segment is the “leader” and which is the “follower” at any given moment, `1366` according to the I3C Specification’s defined behaviors for I3C Devices and how they respond to changing `1367` states. This enables the Isolation Logic to act as a nearly invisible pass-through for I3C transfers, in contrast `1368` to an I3C Bridge Device (which converts I3C transfers to/from actions on another bus or interface), or an I3C `1369` Routing Device (which uses internal queues to store and forward I3C transfers across its Bus segments). 

`1370` The typical use case for a Hub Device assumes that the Active Controller resides on the Upstream Bus `1371` segment, and enables the following types of transfers and other procedures across its Isolation Logic: 

- `1372` • I3C Devices on the Downstream Bus segment can see and participate in transactions initiated on `1373` the Upstream segment, i.e., by the Active Controller, including: 

- `1374` • I3C Broadcast CCCs that are sent to all Targets, where the I3C Devices on the Downstream Bus `1375` segment must ACK the Broadcast Address; 

- `1376` • I3C Direct CCCs that use framing and require specific Targets to provide ACK/NACK, where `1377` the Targets on the Downstream Bus segment must ACK or NACK their Target Address at the `1378` appropriate time, and optionally respond with data (i.e., for Direct Read/GET CCCs); 

- `1379` • I3C modal flows (e.g., Dynamic Address Assignment with ENTDAA), where the I3C Devices `1380` on the Downstream Bus segment must participate in the flows (i.e., arbitrate and eventually `1381` receive a Dynamic Address); 

- `1382` • Private Write transactions in SDR Mode that are directed to Targets that are on the Downstream `1383` Bus segment and will ACK the Write; 

- `1384` • Private Write transactions in SDR Mode that are directed to Group Addresses having at least one `1385` Target assigned to that Group on the Downstream segment that will ACK the write; 

- `1386` • Private Read transactions in SDR Mode that are directed to Targets that are on the Downstream `1387` Bus segment, and for which an ACK with response to the Read will be returned; 

- `1388` • Entering HDR Modes, using the HDR Restart Pattern to frame different transfers in the same `1389` HDR Mode, and driving HDR Generic Write and Read transfers in supported HDR Modes `1390` directed to Targets (and optionally Groups, as above) on the Downstream Bus segment, per the `1391` signaling protocol of that HDR Mode; 

- `1392` • Exiting HDR Modes using the HDR Exit Pattern; 

- `1393` • Error recovery procedures (per _**[MIPI03]**_ at _**Section 4.3.8**_ ) that are meant for all I3C Devices on `1394` both Upstream and Downstream segments, or (optionally) only on the Downstream segment; 

- `1395` • Reset flows that include the Target Reset Pattern (per _**[MIPI03]**_ at _**Section 4.3.9**_ ) that are meant `1396` for all I3C Devices on both Upstream and Downstream segments, or (optionally) only on the `1397` Downstream segment; 

Copyright © 2021–2025 MIPI Alliance, Inc. **Public Release Edition** 

49 

I3C Application Note: Virtual Devices and Virtual Targets 

App Note Version 1.2 29-Aug-2025 

- `1398` • I3C Devices on the Downstream segment can detect defined Bus Conditions (including Bus Idle `1399` and Bus Available, per specification _**Section 4.3.3.2**_ ) and know when they can drive a START `1400` request to initiate various types of In-Band Interrupt requests, including: 

- `1401` • In-Band Interrupt Requests from a Target; 

- `1402` • Hot-Join Requests; and 

- `1403` • Controller Role Requests (although the typical use case for such a Hub Device does not support `1404` an I3C Controller-capable Device on its Downstream Bus segment); 

- `1405` • I3C Devices on the Downstream segment can monitor the Address Header after a START `1406` condition and optionally arbitrate their assigned Dynamic Address into the Arbitrable Address `1407` Header, to drive an In-Band Interrupt Request (as listed above). 

`1408` _**Note:**_ 

- `1409` _**The use cases listed above are not exhaustive** , but are intended to provide an overview of the_ `1410` _kinds of situations that the Isolation Logic would expect to encounter and handle, with the goal of_ `1411` _tracking changes in state on the SDA and SCL lines that connect to both the Upstream and_ `1412` _Downstream segments. The Isolation Logic needs some level of awareness of the I3C electrical_ `1413` _states (i.e., how and when to transition SDA between Open Drain vs. Push-Pull), such that it_ `1414` _accurately replicates to one segment the actions driven by one or more I3C Devices connected to_ `1415` _the other segment. The Isolation Logic designer must assume that the behavior of the I3C Devices_ `1416` _on each Segment conforms to the I3C Specification._ 

- `1417` The Isolation Logic also works with the Peripheral logic to ensure that when transactions from the Upstream `1418` Bus segment are addressed to internal Virtual Targets (such as the Hub Manager Function; see `1419` _**Section 6.4.2**_ above), the Isolation Logic gives priority to the Upstream Bus segment and always treats the `1420` Downstream Bus segment as the “follower”. 

- `1421` Hub Devices with more advanced functionality could provide additional control over the Isolation Logic’s `1422` operating mode, and could support optional requests sent to the Hub Manager Function via a content protocol. `1423` Such optional requests could include: 

- `1424` • Control over when attempts to raise In-Band Interrupt requests from I3C Targets on the `1425` Downstream Bus segment would be allowed vs. not allowed. This could be achieved by: 

- `1426` • Intercepting and overriding the Dynamic Address of such I3C Targets (i.e., by determining when `1427` a START condition or IBI Request has been initiated by a Downstream Target, and then trying `1428` to drive a lower Address value into the Arbitrable Address Header); or 

- `1429` • Providing NACK when the Dynamic Address of a known I3C Target on the Downstream Bus `1430` segment is detected after a START, when the Downstream Target initiated the IBI Request (i.e., `1431` by temporarily disconnecting the Leader/Follower tracking circuit, driving NACK with a clock `1432` cycle, etc.); 

- `1433` • Control over the Isolation Logic’s ability to pass HDR Modes to the Downstream Bus segment, `1434` for situations where the additional propagation delay or other electrical parameters do not support `1435` transfers in some or all HDR Modes, for the specific I3C Devices on the Downstream Bus `1436` segment; 

- `1437` • Control over when the Downstream Bus segment is “parked” and kept in a Bus Idle state (i.e., `1438` when SCL and SDA lines for the segment are pulled to High and stay High) and the Isolation `1439` Logic would not pass any transactions from the Upstream Bus segment; 

- `1440` • Control over whether the Isolation Logic is allowed to pass the HDR Exit Pattern and/or I3C `1441` Target Reset Pattern (either with or without preceding RSTACT CCCs) to the Downstream Bus `1442` segment, when operating in SDR Mode. 

Copyright © 2021–2025 MIPI Alliance, Inc. **Public Release Edition** 

50 

App Note Version 1.2 29-Aug-2025 

I3C Application Note: Virtual Devices and Virtual Targets 

`1443` Hub Devices with more advanced functionality could also support special error recovery commands sent to `1444` the Hub Manager Function via a content protocol. For these special error recovery commands, the Hub `1445` Manager Function could temporarily command the Isolation Logic to disconnect its Leader/Follower tracking `1446` circuit, and then initiate certain error recovery procedures that only affect the Downstream Bus segment. `1447` Such procedures could include: `1448` • Sending START, 7'h7E/W, HDR Exit Pattern followed by STOP to recover from various Target `1449` Errors (per _**[MIPI03]**_ at _**Section 4.3.8.2.3**_ and _**Section 4.3.8.2.5**_ ) for situations when the Isolation `1450` Logic detects that the Leader/Follower tracking circuit definitively determined that at least one `1451` I3C Device on the Upstream Bus segment did provide ACK to the Broadcast Address, but no I3C `1452` Devices on the Downstream Bus segment provided ACK to the Broadcast Address. 

- `1453` • For such cases, the Isolation Logic must determine whether such an ACK was seen on earlier `1454` occasions from any I3C Devices on the Downstream Bus segment. 

- `1455` • If the Isolation Logic also has the ability to proactively monitor for such situations (i.e., loss of `1456` Broadcast ACK on the Downstream Bus segment), then the Peripheral logic and Hub Manager `1457` Function could also generate an In-Band Interrupt Request to the Active Controller with a `1458` notification of that condition. 

- `1459` • Stuck SDA Handling (per _**[MIPI03]**_ at _**Section 4.3.8.2.6**_ ) for situations when the Isolation Logic `1460` detects an I3C Device holding SDA High or Low on the Downstream Bus segment, and `1461` automatically disconnects its Leader/Follower tracking circuit accordingly (i.e., to protect the `1462` Upstream Bus segment). 

- `1463` • For situations where the Isolation Logic must automatically disconnect its Leader/Follower `1464` tracking circuit to protect the Upstream Bus segment, the Peripheral logic and Hub Manager `1465` function could generate an In-Band Interrupt Request to the Active Controller with a notification `1466` of that condition. 

- `1467` • Target Reset flows using the Target Reset Pattern, with zero or more preceding RSTACT CCCs in `1468` a sequence (per _**[MIPI03]**_ at _**Section 4.3.9**_ ) sent to I3C Target(s) on the Downstream Bus segment `1469` only, but not visible to any I3C Devices on the Upstream Bus segment. 

- `1470` • Direct reset pin control or power management of one or more I3C Devices on the Downstream `1471` Bus segment, using special reset and power control logic that could force such I3C Devices to be `1472` reset or power-cycled in extreme cases of failure or non-response. 

- `1473` • This would also require additional GPIO outputs (for reset pin control) or power relay circuits `1474` (for power management) that could be controlled via the content protocol. 

Copyright © 2021–2025 MIPI Alliance, Inc. **Public Release Edition** 

51 

I3C Application Note: Virtual Devices and Virtual Targets 

App Note Version 1.2 29-Aug-2025 

## `1475` **6.4.4 Support for Open Drain Pull-Up Handling** 

`1476` For some system designs, the Downstream Bus segment might require a special Pull-Up value due to the `1477` number of Target Devices that must be isolated from the Upstream Bus segment, and the overall design of `1478` the Downstream Bus (see I3C electrical parameter **RP** , per _**[MIPI03]**_ at _**Section 4.3.11.1**_ ). In such situations, `1479` the I3C Hub Device must provide the appropriate Pull-Up for Open Drain mode for its Downstream Bus `1480` segment, per the I3C Specification. Parameter **RP** for the Downstream Bus segment needs to be chosen `1481` carefully because the Hub Device does not store and forward I3C transfers (as an I3C Routing Device would `1482` do). This means that all Private Write/Read transfers initiated by the Active Controller on the Upstream Bus `1483` segment must necessarily happen at the same data transfer rate on the Downstream Bus segment. 

`1484` The Hub Device must either detect when the Active Controller on the Upstream Bus segment is using its own `1485` Pull-Up; or the Hub Device could utilize an external Pull-Up control pin provided by the Active Controller `1486` for this purpose (if available). The I3C Specification does allow an I3C Controller Device to provide an `1487` external pin for Open Drain Pull-Up (see _**[MIPI03]**_ at _**Section 4.3.3.1**_ and _**Section 4.3.11.1**_ ); this pin can the `1488` Controller’s sole source of Pull-Up, or it can be in addition to an internal Open Drain class Pull-Up structure `1489` (e.g., an internal Pull-Up resistor or current source which is only engaged or enabled for Open Drain mode). 

`1490` _**Figure 13**_ shows a partial view of an example Hub Device (derived from a portion of _**Figure 12**_ ) with a `1491` direct pin connection to the Active Controller of the Upstream Bus segment (i.e., the Primary Controller). `1492` The Hub Device monitors this direct pin connection, and selectively enables or disables its own Open Drain `1493` class Pull-Up for its Downstream Bus segment in response to the signal driven by the Active Controller (as `1494` well as other conditions detected by the Leader/Follower tracking circuit). In this example, the Open Drain `1495` class Pull-Up for the Downstream Bus segment can either be internal to the Hub Device, or external (i.e., a `1496` Pull-Up resistor controlled by an output pin in the I/O pads facing the Downstream Bus segment). Such a `1497` design allows the Hub Device to be tuned to the specific needs of the Downstream Bus segment and its Target `1498` Devices. 

```
1499
```

**==> picture [278 x 168] intentionally omitted <==**

**----- Start of picture text -----**<br>
SDA<br>I3C<br>PRIMARY<br>CONTROLLER SCL<br>ACTIVE<br>External Pull-Up pin<br>PWR<br>GND<br>I/O PERIPHERAL<br>Pull-Up<br>class (OD)<br>Hub Manager  Isolation<br>Function Logic To Isolated<br>Segment<br>**----- End of picture text -----**<br>


**Figure 13 I3C Hub Device using External Pin for Open Drain Pull-Up** 

```
1500
```

## _**Note:**_ 

`1501` _Per the I3C Specification, each Bus segment also requires a High-Keeper Pull-Up (see_ _**[MIPI03]** at_ `1502` _**Section 4.3.3.1** ), however these High-Keeper Pull-Ups are not shown in_ _**Figure 13** . If the Hub Device_ `1503` _also provides the High-Keeper Pull-Up, then it can be either internal or external. The Hub Device_ `1504` _must also disengage both Pull-Ups (i.e., for High-Z) as necessary when it detects certain types of_ `1505` _Handoff transitions._ `1506` _An I3C Controller Device that provides an external Pull-Up for Open Drain will typically use this pin_ `1507` _to control an external Pull-Up resistor for the Upstream Bus segment. This Pull-Up resistor is also_ `1508` _not shown in_ _**Figure 13** ._ 

Copyright © 2021–2025 MIPI Alliance, Inc. **Public Release Edition** 

52 

