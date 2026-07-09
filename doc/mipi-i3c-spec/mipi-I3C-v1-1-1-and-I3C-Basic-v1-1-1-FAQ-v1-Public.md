## **Frequently Asked Questions (FAQ) for MIPI I3C[®] v1.1.1 & MIPI I3C Basic[SM] v1.1.1** 

**FAQ Version 1.1 22 August 2022** 

MIPI Board Approved 22 August 2022 **Public Release Edition** 

This is an informative document, not a MIPI Specification. Various rights and obligations that apply solely to MIPI Specifications (as defined in the MIPI Membership Agreement and MIPI Bylaws) including, but not limited to, patent license rights and obligations, do not apply to this document. 

This document is subject to further editorial and technical development. 

Copyright © 2018–2022 MIPI Alliance, Inc. 

FAQ for MIPI I3C v1.1.1 & MIPI I3C Basic v1.1.1 

FAQ Version 1.1 22-Aug-2022 

## **NOTICE OF DISCLAIMER** 

The material contained herein is provided on an “AS IS” basis. To the maximum extent permitted by applicable law, this material is provided AS IS AND WITH ALL FAULTS, and the authors and developers of this material and MIPI Alliance Inc. (“MIPI”) hereby disclaim all other warranties and conditions, either express, implied or statutory, including, but not limited to, any (if any) implied warranties, duties or conditions of merchantability, of fitness for a particular purpose, of accuracy or completeness of responses, of results, of workmanlike effort, of lack of viruses, and of lack of negligence. ALSO, THERE IS NO WARRANTY OR CONDITION OF TITLE, QUIET ENJOYMENT, QUIET POSSESSION, CORRESPONDENCE TO DESCRIPTION OR NON-INFRINGEMENT WITH REGARD TO THIS MATERIAL. 

IN NO EVENT WILL ANY AUTHOR OR DEVELOPER OF THIS MATERIAL OR MIPI BE LIABLE TO ANY OTHER PARTY FOR THE COST OF PROCURING SUBSTITUTE GOODS OR SERVICES, LOST PROFITS, LOSS OF USE, LOSS OF DATA, OR ANY INCIDENTAL, CONSEQUENTIAL, DIRECT, INDIRECT, OR SPECIAL DAMAGES WHETHER UNDER CONTRACT, TORT, WARRANTY, OR OTHERWISE, ARISING IN ANY WAY OUT OF THIS OR ANY OTHER AGREEMENT RELATING TO THIS MATERIAL, WHETHER OR NOT SUCH PARTY HAD ADVANCE NOTICE OF THE POSSIBILITY OF SUCH DAMAGES. 

The material contained herein is not a license, either expressly or impliedly, to any IPR owned or controlled by any of the authors or developers of this material or MIPI. Any license to use this material is granted separately from this document. This material is protected by copyright laws, and may not be reproduced, republished, distributed, transmitted, displayed, broadcast or otherwise exploited in any manner without the express prior written permission of MIPI Alliance. MIPI, MIPI Alliance and the dotted rainbow arch and all related trademarks, service marks, tradenames, and other intellectual property are the exclusive property of MIPI Alliance Inc. and cannot be used without its express prior written permission. The use or implementation of this material may involve or require the use of intellectual property rights (“IPR”) including (but not limited to) patents, patent applications, or copyrights owned by one or more parties, whether or not members of MIPI. MIPI does not make any search or investigation for IPR, nor does MIPI require or request the disclosure of any IPR or claims of IPR as respects the contents of this material or otherwise. 

Without limiting the generality of the disclaimers stated above, users of this material are further notified that MIPI: (a) does not evaluate, test or verify the accuracy, soundness or credibility of the contents of this material; (b) does not monitor or enforce compliance with the contents of this material; and (c) does not certify, test, or in any manner investigate products or services or any claims of compliance with MIPI specifications or related material. 

Questions pertaining to this material, or the terms or conditions of its provision, should be addressed to: 

MIPI Alliance, Inc. 

c/o IEEE-ISTO 

445 Hoes Lane, Piscataway New Jersey 08854, United States Attn: Managing Director 

## **Special Note Concerning MIPI I3C and MIPI I3C Basic** 

As described in the I3C Basic specification, certain parties have agreed to grant additional rights to I3C Basic implementers, beyond those rights granted under the MIPI Membership Agreement or MIPI Bylaws. Contribution to or other participation in the development of this FAQ document does not create any implication that a party has agreed to grant any additional rights in connection with I3C Basic. Consistent with the statements above, nothing in or about this FAQ document alters any party’s rights or obligations associated with I3C or I3C Basic. 

ii 

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

FAQ Version 1.1 22-Aug-2022 

FAQ for MIPI I3C v1.1.1 & MIPI I3C Basic v1.1.1 

## **Contents** 

|**Release**|**History ................................................................................................................. ix**|
|---|---|
|**1**|**Introduction .........................................................................................................1**|
|**2**|**Frequently Asked Questions ..............................................................................3**|
|**General**|**Questions ..............................................................................................................4**|
|**2.1**|**Introduction to MIPI I3C .............................................................................................. 4**|
|Q1.1|What is MIPI I3C and I3C Basic? .................................................................................... 4|
|Q1.2|What does the I3C acronym mean? .................................................................................. 4|
|Q1.3|Why is MIPI I3C being introduced? ................................................................................. 4|
|Q1.4|What are the main features of MIPI I3C? ......................................................................... 4|
|Q1.5|For which applications or use cases is I3C intended to be used? ...................................... 4|
|Q1.6|How can the MIPI I3C specifications be obtained? .......................................................... 4|
|**2.2**|**Migration from Legacy I2C or Other Buses ................................................................ 5**|
|Q2.1|Why replace I2C with I3C? ............................................................................................... 5|
|Q2.2|Does I3C use less power than I²C? ................................................................................... 5|
|Q2.3|How is I3C different from I²C? ......................................................................................... 5|
|Q2.4|Why replace SPI (Serial Peripheral Interface) with I3C? ................................................. 5|
|**2.3**|**I3C Versions and Releases ............................................................................................. 5**|
|Q3.1|What is new in I3C v1.1? .................................................................................................. 5|
|Q3.2|What are the required features in I3C v1.1 vs. I3C 1.0? ................................................... 6|
|Q3.3|Are there any I3C v1.0 features that are not supported in I3C v1.1 and beyond? ............ 6|
|Q3.4|What is new in MIPI I3C v1.1.1? ..................................................................................... 6|
|Q3.5|Is I3C v1.1.1 compatible/interoperable with I3C v1.1? .................................................... 7|
|Q3.6|What is new in I3C Basic v1.1.1? ..................................................................................... 7|
|**2.4**|**Up and Coming .............................................................................................................. 8**|
|Q4.1|What future MIPI specifications will be leveraging I3C? ................................................. 8|
|Q4.2|Are there any impending fixes or errata for MIPI I3C v1.0 or I3C Basic v1.0 that should|
||be applied now? ................................................................................................................ 8|
|Q4.3|Are any revisions to MIPI I3C v1.0 expected? ................................................................. 8|
|Q4.4|Are there any impending fixes or errata for MIPI I3C v1.1 that should be applied now? 8|
|Q4.5|Are any revisions to I3C v1.1 expected? .......................................................................... 9|
|Q4.6|Are any revisions to I3C v1.1.1 expected? ....................................................................... 9|
|Q4.7|Are there any impending fixes or errata for I3C v1.1.1 and I3C Basic v1.1.1 that should|
||be applied now? ................................................................................................................ 9|
|Q4.8|What new features, if any, are coming to MIPI I3C? ...................................................... 10|
|**2.5**|**Naming and Terminology ............................................................................................ 11**|
|Q5.1|What is an I3C “Controller” Device, and why was the I3C “Master” Device renamed? 11|
|Q5.2|What is an I3C “Target” Device, and why was the I3C “Slave” Device renamed? ........ 11|



Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

|FAQ for MIPI I3C v1.1.1 & MIPI I3C Basic v1.1.1<br>FAQ Version 1.1|FAQ for MIPI I3C v1.1.1 & MIPI I3C Basic v1.1.1<br>FAQ Version 1.1|
|---|---|
||22-Aug-2022|
|**2.6**|**Implementation: Ecosystem ........................................................................................ 12**|
|Q6.1|Who is defining the MIPI I3C Specifications? ............................................................... 12|
|Q6.2|Is anyone currently using I3C? ....................................................................................... 12|
|Q6.3|What is the availability of development hardware for I3C prototyping, including|
||FPGAs? ........................................................................................................................... 12|
|Q6.4|What is the I3C IP core availability in the market? ........................................................ 12|
|**2.7**|**Implementation: As a System Designer ..................................................................... 13**|
|Q7.1|What is the maximum capacitance load allowed on the I3C Bus? ................................. 13|
|Q7.2|What is the maximum wire length for I3C communication? .......................................... 13|
|Q7.3|Can I2C repeaters be used for I3C? ................................................................................. 13|
|Q7.4|Will the I2C devices respond to I3C commands? ............................................................ 13|
|Q7.5|How are communication conflicts resolved on the I3C Bus? ......................................... 13|
|Q7.6|Can I3C Devices cause the communication Bus to hang? .............................................. 13|
|Q7.7|Will all I3C Devices be compatible with all CCCs? ....................................................... 13|
|**2.8**|**Implementation: As a Software Developer ................................................................ 14**|
|Q8.1|Are there any companion MIPI I3C Specifications that enable software development? 14|
|Q8.2|Are there software libraries available for I3C? ............................................................... 14|
|**2.9**|**Interoperability Workshops ........................................................................................ 15**|
|Q9.1|What is a MIPI I3C Interoperability Workshop? ............................................................ 15|
|Q9.2|What is the output from a MIPI I3C Interoperability Workshop? ................................... 15|
|Q9.3|Are MIPI I3C Interoperability Workshops an ongoing activity? .................................... 15|
|Q9.4|Who can attend or participate in a MIPI I3C Interoperability Workshop? ..................... 15|
|Q9.5|What HW/SW is typically needed to participate in a MIPI I3C Interoperability|
||Workshop? ...................................................................................................................... 15|
|Q9.6|Are there any I3C Interoperability Workshops planned for I3C v1.1.1 or I3C Basic|
||v1.1.1? ............................................................................................................................. 15|
|**2.10**|**Conformance Testing ................................................................................................... 16**|
|Q10.1|What is a MIPI Conformance Test Suite (CTS)? ............................................................ 16|
|Q10.2|Is there a MIPI CTS for I3C? .......................................................................................... 16|
|Q10.3|What is the scope of tests for the I3C CTS? ................................................................... 16|
|Q10.4|Does the I3C Interoperability Workshop follow the I3C CTS? ...................................... 16|
|Q10.5|What details are provided for each I3C CTS test case? .................................................. 16|
|**2.11**|**Legal and Intellectual Property Related Questions .................................................. 17**|
|Q11.1|Is MIPI I3C Basic royalty free? ...................................................................................... 17|
|Q11.2|What license terms apply to MIPI I3C v1.x? .................................................................. 17|
|**Detailed**|**Technical Questions ..........................................................................................18**|
|**2.12**|**New Capabilities in I3C ............................................................................................... 18**|
|Q12.1|Can I3C Targets initiate communication (i.e., interrupt the Controller)? ........................ 18|
|Q12.2|How can Controllers and Targets communicate on the I3C Bus? ................................... 18|
|Q12.3|What are CCCs (Common Command Codes) and why are they used? .......................... 18|
|Q12.4|How are the following similar and/or different: In-Band Interrupt, Hot-Join, and|
||Controller Role Request (IBI / HJ / CRR)? .................................................................... 18|



iv 

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

FAQ Version 1.1 

FAQ for MIPI I3C v1.1.1 & MIPI I3C Basic v1.1.1 

22-Aug-2022 

|**2.13**|**Limits and Performance .............................................................................................. 19**|
|---|---|
|Q13.1|What is the maximum number of I3C Devices per Bus? ................................................ 19|
|Q13.2|Can there be more than one I3C Target inside a chip? .................................................... 19|
|Q13.3|What is the bit rate for I3C? ............................................................................................ 19|
|Q13.4|Is it possible to have multiple Controllers on the same I3C Bus? ................................... 20|
|Q13.5|Can a Target indicate any speed limit that it might have? ............................................... 20|
|Q13.6|Is there a maximum limit to I3C Bus payload length? .................................................... 20|
|**2.14**|**Minimum Required Features ...................................................................................... 21**|
|Q14.1|Which features are required for a Device to be a compliant I3C Controller? ................. 21|
|Q14.2|Which features are required for a Device to be a compliant I3C Target? ....................... 21|
|**2.15**|**Backwards Compatibility with I2C ............................................................................ 22**|
|Q15.1|Is I3C backward compatible with I²C? ........................................................................... 22|
|Q15.2|Can I3C Devices operate on a Legacy I2C Bus? ............................................................. 22|
|Q15.3|Can I3C and I²C co-exist on the same bus? .................................................................... 22|
|Q15.4|How does an I3C Target behave with an I2C Controller vs. with an I3C Controller? ..... 22|
|**2.16**|**Address Assignment ..................................................................................................... 23**|
|Q16.1|Are all I3C Targets required to support Dynamic Address Assignment with the|
||ENTDAA CCC? ............................................................................................................. 23|
|Q16.2|How can an I3C Target lose its I3C Dynamic Address, and how does it become an I2C|
||Target again? ................................................................................................................... 23|
|Q16.3|What is a Provisioned ID, and why is it needed? ............................................................ 23|
|Q16.4|How do the first 32 bits of the Provisioned ID (PID) work? Are they random or fixed? 24|
|Q16.5|What if the Controller detects a collision during Dynamic Address Assignment with the|
||ENTDAA CCC? ............................................................................................................. 24|
|Q16.6|What CCCs must an I3C Target support before a Dynamic Address is assigned?.......... 24|
|Q16.7|What implicit state or configuration is required for an I3C Device that supports Group|
||Addressing? .................................................................................................................... 25|
|Q16.8|Can any CCCs change or override an I3C Target’s assigned Dynamic Address? ........... 25|
|Q16.9|Are I3C Targets required to provide ACK for Broadcast CCCs that are not supported? 26|
|**2.17**|**In-Band Interrupt and Hot-Join ................................................................................ 26**|
|Q17.1|What changed with In-Band Interrupts (IBIs) in I3C v1.1.1? ......................................... 26|
|Q17.2|How can an I3C Controller support Pending Read Notifications? ................................. 27|
|Q17.3|What is Hot-Join? ........................................................................................................... 27|
|Q17.4|Is an I3C Target required to receive and process the Broadcast ENEC, DISEC, and other|
||Bus-state CCCs before sending a Hot-Join Request, or before being assigned a Dynamic|
||Address?.......................................................................................................................... 27|
|Q17.5|Is an I3C Target required to wait the full 1 ms before it can send a Hot-Join Request? . 28|
|Q17.6|Can I3C Hot-Join Target Devices be used on a Legacy I2C bus? ................................... 28|
|Q17.7|Can an I3C Target support Hot-Join when used on an I3C Bus, and still function|
||correctly on a Legacy I2C Bus?....................................................................................... 28|
|Q17.8|Can multiple I3C Targets use the same reserved Hot-Join Address, or can multiple Hot-|
||Joining I3C Targets raise a Hot-Join Request at the same time? .................................... 29|
|Q17.9|In a Hot-Join, when should the DISEC CCC be sent? After ACK, or after NACK? ...... 29|
|Q17.10 What has changed regarding Hot-Join in I3C v1.1.1? .................................................... 30||
|**2.18**|**Common Command Codes (CCCs) ........................................................................... 31**|



Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

FAQ for MIPI I3C v1.1.1 & MIPI I3C Basic v1.1.1 

|Q for MIPI I3C v1.1.1 & MIPI I3C Basic v1.1.1<br>FAQ Version 1.1|Q for MIPI I3C v1.1.1 & MIPI I3C Basic v1.1.1<br>FAQ Version 1.1|
|---|---|
||22-Aug-2022|
|Q18.1|What are the differences between I3C v1.0 and I3C v1.1 in how CCCs are defined? .... 31|
|Q18.2|Does the mandated "single-retry model" apply to all Directed Read CCCs? ................. 32|
|Q18.3|What has changed in CCC use or coding in I3C v1.1 or v1.1.1? .................................... 32|
|Q18.4|What are Vendor / Standard Extension CCCs, who can use them, and how are they|
||differentiated among different uses? ............................................................................... 34|
|Q18.5|How should custom CCCs be used as part of a content protocol based on I3C? ............ 34|
|Q18.6|What is the new Command Code value 0x1F for CCCs, and how should it be used?.... 36|
|Q18.7|Which Dynamic Address Assignment CCCs is a Device required to support? .............. 36|
|Q18.8|Why was the RSTDAA Directed CCC deprecated, and why is it being removed? ........ 37|
|Q18.9|How is the GETMXDS CCC (maximum data speed) updated in I3C v1.1? .................. 37|
|Q18.10 For Secondary Controller Devices, which format of the GETMXDS Direct CCC is used||
||with the MSTHDLY Defining Byte? .............................................................................. 37|
|Q18.11 What is the new GETACCCR CCC, and how is it different from the GETACCMST||
||CCC? ............................................................................................................................... 37|
|Q18.12 What is the new DEFTGTS CCC, and how is it different from the DEFSLVS CCC? ... 37||
|Q18.13 Why has the figure for the GETCAPS CCC changed? ................................................... 37||
|Q18.14 Why have some of the Defining Byte names changed for the GETCAPS, GETSTATUS,||
||and GETMXDS CCCs? .................................................................................................. 37|
|Q18.15 Where is the Defining Byte for the SETXTIME CCC? .................................................. 38||
|Q18.16 What has changed with the ENDXFER CCC for HDR-TSP and HDR-TSL Modes? .... 38||
|Q18.17 What has changed with the MLANE CCC and Multi-Lane Device configuration? ....... 38||
|Q18.18 How should implementers determine the minimum values for Set Max Write Length||
||(SETMWL) and Set Max Read Length (SETMRL)? ..................................................... 39|
|Q18.19 Do the configured Max Write Length and Max Read Length values apply to HDR||
||Modes? ............................................................................................................................ 39|
|Q18.20 How does the Target respond to the GETSTATUS CCC if the Controller sends||
||ENEC/DISEC CCCs to enable or disable In-Band Interrupts? ....................................... 40|
|Q18.21 In the DEFTGTS CCC data bytes, where are the padding bits for the Controller’s||
||Addresses? ...................................................................................................................... 40|
|**2.19**|**High Data Rate (HDR) Modes .................................................................................... 41**|
|Q19.1|Does Figure 44 HDR-DDR Format apply for Command, Data, and CRC? Or only for|
||Data? ............................................................................................................................... 41|
|Q19.2|Does the Controller provide an additional CLK after the Terminate Condition and before|
||the Restart/Exit Pattern, as shown in Figure 52 Controller Terminates Read? ............... 41|
|Q19.3|During HDR-DDR Mode CRC 5 transmission, how many clocks should the Target|
||expect to receive? ............................................................................................................ 41|
|Q19.4|For HDR-DDR Mode transfers, how should the Controller manage the Pull-Ups at the|
||end of the HDR-DDR Command Word? ........................................................................ 42|
|Q19.5|In HDR-DDR Mode, how do Controllers and Targets enable flow control for NACK? 42|
|Q19.6|What has changed regarding HDR Modes in I3C v1.1.1? .............................................. 43|
|Q19.7|What has changed regarding HDR Ternary Modes in I3C v1.1.1? ................................. 43|
|Q19.8|What has changed regarding HDR-BT Mode in I3C v1.1.1? ......................................... 43|
|Q19.9|Are there any issues with the HDR-BT diagrams? ......................................................... 44|
|Q19.10 What is the HDR-BT Data Block Delay mechanism? .................................................... 45||
|**2.20**|**I3C Advanced Capabilities .......................................................................................... 46**|



vi 

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

FAQ Version 1.1 

FAQ for MIPI I3C v1.1.1 & MIPI I3C Basic v1.1.1 

|22-Aug-2022|22-Aug-2022||
|---|---|---|
|Q20.1||What is Offline, and what does it mean to be Offline Capable? ..................................... 46|
|Q20.2||What is a Virtual Target? ................................................................................................. 46|
|Q20.3||Does the I3C Bus support Bridges? ................................................................................ 46|
|Q20.4||How does the Set Bridge Targets (SETBRGTGT) CCC differ between I3C v1.0 and I3C|
|||v1.1+? ............................................................................................................................. 47|
|Q20.5||Does the I3C Bus enable Routing? ................................................................................. 47|
|Q20.6||Why does I3C allow more than one Controller on the I3C Bus? What can a Secondary|
|||Controller do that the Primary Controller can’t? ............................................................ 47|
|Q20.7||Is any time-stamping capability defined for the I3C Bus? .............................................. 48|
|Q20.8||Can Synchronous and Asynchronous Timing Control both be enabled at the same time?|
|||........................................................................................................................................ 48|
|Q20.9||Is there a way to turn off Timing Control? ...................................................................... 48|
|Q20.10||What has changed regarding Multi-Lane for SDR Mode? ............................................. 49|
|**2.21**|**Electricals and Signaling ............................................................................................. 50**||
|Q21.1||How many signal lines does I3C have? .......................................................................... 50|
|Q21.2||Does I3C require Pull-Up resistors on the bus like I²C? ................................................. 50|
|Q21.3||When is the Pull-Up resistor enabled? ............................................................................ 50|
|Q21.4||Is a High-Keeper needed for the I3C Bus? ..................................................................... 50|
|**2.22**|**Bus Conditions and States ........................................................................................... 51**||
|Q22.1||What are some of the I3C Bus conditions when the Bus is considered inactive? ........... 51|
|Q22.2||When an I3C Device wishes to send an In-Band Interrupt (IBI) Request, does it need to|
|||see a STOP before a Bus Idle? ........................................................................................ 51|
|Q22.3||When can an I3C Target issue an In-Band Interrupt (IBI) Request? .............................. 51|
|Q22.4||What are the I3C Bus Activity States? ............................................................................ 51|
|**2.23**|**Resets and Error Handling ......................................................................................... 52**||
|Q23.1||Are there any test modes in the I3C Bus? ....................................................................... 52|
|Q23.2||Are there any error detection and recovery methods in I3C? ......................................... 52|
|Q23.3||What happens if the Controller crashes during a Read? ................................................. 52|
|Q23.4||Is there any way to exit from an Error of Type TE0 or TE1, other than waiting for an|
|||Exit Pattern? .................................................................................................................... 52|
|Q23.5||Can a Controller issue a STOP condition regardless of whether or not a Target has issued|
|||an acknowledgment indicating a completed transaction? ............................................... 52|
|Q23.6||What errors are reported on the GETSTATUS Protocol Error bit? ................................. 52|
|Q23.7||What errors does Target Error Type TE5 cover? ............................................................. 53|
|Q23.8||Are Devices required to wait for a Repeated START or STOP, or both, to recover from|
|||Error Types TE2–TE5? ................................................................................................... 53|
|Q23.9||What has changed regarding Target Error Types in I3C v1.1.1? .................................... 54|
|Q23.10||When does the RSTACT CCC state clear in an I3C Target? .......................................... 54|
|Q23.11||What is the minimal Target Reset support required in I3C v1.1 or v1.1.1? .................... 54|
|Q23.12||When does a Target escalate Target Reset to Full/Chip Reset? ....................................... 54|
|Q23.13||How is Target escalation affected when the RSTACT CCC is received? ....................... 55|
|**2.24**|**Timing Parameters ...................................................................................................... 56**||
|Q24.1||Are there any special timing requirements for sending the first START with the|
|||Broadcast Address? ......................................................................................................... 56|



Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

vii 

|FAQ for MIPI I3C v1.1.1 & MIPI I3C Basic v1.1.1<br>FAQ Version 1.1|FAQ for MIPI I3C v1.1.1 & MIPI I3C Basic v1.1.1<br>FAQ Version 1.1|
|---|---|
||22-Aug-2022|
|Q24.2|What is the I3C Open-Drain tHighMax? Table 10 shows it as 41 ns, but a Note says it|
||may be longer .................................................................................................................. 56|
|Q24.3|How should tSCOtiming be interpreted? .......................................................................... 56|
|Q24.4|If a Device has a tSCOvalue greater than 12 ns, does that mean it doesn’t qualify as an|
||I3C Device? .................................................................................................................... 56|
|Q24.5|How do tCBSrand tCASrtiming differ between I3C v1.1 and I3C v1.0? ........................... 57|
|Q24.6|Are there any special timing parameters for sending the HDR Exit Pattern, HDR Restart|
||Pattern or Target Reset Pattern? ...................................................................................... 57|
|**3**|**Terminology .......................................................................................................58**|
|**3.1**|**Definitions ..................................................................................................................... 58**|
|**3.2**|**Abbreviations ............................................................................................................... 58**|
|**3.3**|**Acronyms ...................................................................................................................... 59**|
|**4**|**References ..........................................................................................................60**|



. 

viii 

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

FAQ Version 1.1 22-Aug-2022 

FAQ for MIPI I3C v1.1.1 & MIPI I3C Basic v1.1.1 

## **Release History** 

|**Release**|**History**||
|---|---|---|
|**Date**|**Version**|**Description**|
|04-Sep-2021|FAQ v1.0|Initial Board Approved release.|
|22-Aug-2022|FAQ v1.1|Board Approved release.|



Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

ix 

FAQ for MIPI I3C v1.1.1 & MIPI I3C Basic v1.1.1 

FAQ Version 1.1 22-Aug-2022 

This page intentionally left blank. 

Copyright © 2018–2022 MIPI Alliance, Inc. 

x 

**Public Release Edition** 

FAQ Version 1.1 22-Aug-2022 

FAQ for MIPI I3C v1.1.1 & MIPI I3C Basic v1.1.1 

## **1 Introduction** 

- `1` This FAQ has been developed to introduce the MIPI I3C _**[MIPI01][MIPI11][MIPI13]**_ and I3C Basic `2` _**[MIPI09][MIPI14]**_ specifications to developers and users. The I3C WG has compiled these frequently asked `3` questions (FAQs) to assist Member implementation activity. Some areas also include clarification when an `4` area of the specification was ambiguous, and this FAQ will show the intended resolution of the ambiguity. 

- `5` For I3C v1.1.1 _**[MIPI13]**_ and I3C Basic v1.1.1 _**[MIPI14]**_ , new FAQs have been added, and the existing FAQs `6` have been updated as needed. Some FAQs show historical information for context, i.e., from older versions `7` of I3C or I3C Basic. 

- `8` _**Note:**_ 

`9` _**For the full MIPI I3C Specification, the most current version is I3C v1.1.1.** FAQ entries reflect all updates, both technical and editorial (i.e., the changes from I3C v1.0 or v1.1 to v1.1.1)._ 

```
10
```

`11` _**For the MIPI I3C Basic Specification, the most current version is I3C Basic v1.1.1.** FAQ entries_ `12` _reflect all updates, both technical and editorial (i.e., the changes from I3C Basic v1.0 to v1.1.1). Note_ `13` _that_ _**there is no I3C Basic v1.0** ; this version number was skipped._ 

- `14` Throughout this FAQ document, unless otherwise noted, the terms ‘MIPI I3C’ and ‘I3C’ refer to both MIPI `15` I3C _**[MIPI01][MIPI11][MIPI13]**_ and MIPI I3C Basic _**[MIPI09][MIPI14]**_ , unless specified otherwise. 

- `16` _**Note:**_ 

- `17` _Unless otherwise noted, a reference to a numbered section of the MIPI I3C specification applies to_ `18` _both the I3C Specification and the I3C Basic Specification (i.e., section numbers are aligned across_ `19` _the two specifications)._ 

- `20` 

```
21
```

_None of the answers in this FAQ are intended to overwrite or overrule the information in either the I3C Specification_ _**[MIPI01][MIPI11][MIPI13]** or the I3C Basic Specification_ _**[MIPI09][MIPI14]** ._ 

`22` The FAQ questions are organized into Sections by topic, and grouped into two higher-level categories: `23` general questions about MIPI I3C and the ecosystem; and detailed technical questions about material in the `24` I3C specifications. 

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

FAQ for MIPI I3C v1.1.1 & MIPI I3C Basic v1.1.1 

FAQ Version 1.1 22-Aug-2022 

|**Section**|**Title**|**Focus**|
|---|---|---|
|**2.1**|**Introduction to MIPI I3C**|I’ve heard about I3C. Where can I read a bit more about<br>it?|
|**2.2**|**Migration from Legacy I2C or Other Buses**|What are some of the key reasons to upgrade to I3C<br>from other Buses?|
|**2.3**|**I3C Versions and Releases**|What versions of I3C or I3C Basic have been released,<br>and what has changed?|
|**2.4**|**Up and Coming**|Questions related to the next revision (and/or Errata) of<br>the I3C specification.|
|**2.5**|**Naming and Terminology**|Questions related to recent changes to I3C terminology|
|**2.6**|**Implementation: Ecosystem**|Questions related to design kits, IP, test, and other parts<br>of the enablement ecosystem.|
|**2.7**|**Implementation: As a System Designer**|Questions asked by early system designers.|
|**2.8**|**Implementation: As a Software Developer**|Questions asked by early software developers.|
|**2.9**|**Interoperability Workshops**|Questions asked by early Interoperability Workshop<br>participants.|
|**2.10**|**Conformance Testing**|Questions related to testing device conformance to the<br>I3C specification.|
|**2.11**|**Legal and Intellectual Property Related**<br>**Questions**|Questions related to legal and IPR aspects of the I3C<br>and I3C Basic specifications and implementations.|
|**2.12**|**New Capabilities in I3C**|What new capabilities does I3C bring for key use cases?|
|**2.13**|**Limits and Performance**|What limits or restrictions should be observed on I3C<br>Buses?|
|**2.14**|**Minimum Required Features**|What must all I3C Controllers and Targets support?|
|**2.15**|**Backwards Compatibility with I2C **|How can I3C Devices interoperate with Legacy I2C<br>Buses?|
|**2.16**|**Address Assignment**|What do I3C Devices need to understand regarding<br>Dynamic Addresses?|
|**2.17**|**In-Band Interrupt and Hot-Join**|How can I3C Targets raise Interrupts on an I3C Bus or<br>join an I3C Bus?|
|**2.18**|**Common Command Codes (CCCs)**|What are Common Command Codes, how can they be<br>used, and what details need to be understood by system<br>integrators?|
|**2.19**|**High Data Rate (HDR) Modes**|How can HDR Modes be used to improve data transfer<br>speeds, and what implementation challenges should be<br>addressed?|
|**2.20**|**I3C Advanced Capabilities**|How can I3C’s other optional capabilities extend an I3C<br>Bus to meet challenging new requirements for special<br>use cases?|
|**2.21**|**Electricals and Signaling**|I’ve started to read the I3C specification. Tell me a more<br>about the electrical and signaling, and how to design a<br>system for I3C Devices.|
|**2.22**|**Bus Conditions and States**|What requirements do I3C Devices need to understand<br>for Bus activity and states?|
|**2.23**|**Resets and Error Handling**|How should I3C Controllers and Targets detect errors,<br>and how to recover from errors with defined reset<br>methods?|
|**2.24**|**Timing Parameters**|I need more guidance on the specific timing parameters<br>in the I3C specification.|



Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

2 

FAQ Version 1.1 22-Aug-2022 

FAQ for MIPI I3C v1.1.1 & MIPI I3C Basic v1.1.1 

## **2 Frequently Asked Questions** 

`25` This FAQ is organized into topics by general area and I3C features/capabilities: 

- `26` **General Questions** 

- `27` _**Section 2.1: Introduction to MIPI I3C**_ 

- `28` _**Section 2.2: Migration from Legacy I2C or Other Buses**_ `29` _**Section 2.3: I3C Versions and Releases**_ 

- `30` _**Section 2.4: Up and Coming**_ 

- `31` _**Section 2.5: Naming and Terminology**_ `32` _**Section 2.6: Implementation:**_ Ecosystem `33` _**Section 2.7: Implementation: As a System Designer**_ 

- `34` _**Section 2.8: Implementation: As a Software Developer**_ `35` _**Section 2.9: Interoperability Workshops**_ 

- `36` _**Section 2.10 Conformance Testing**_ 

- `37` _**Section 2.11: Legal and Intellectual Property Related Questions**_ 

- `38` **Detailed Technical Questions** 

- `39` _**Section 2.12: New Capabilities in I3C**_ 

- `40` _**Section 2.13: Limits and Performance**_ `41` _**Section 2.14: Minimum Required Features**_ `42` _**Section 2.15: Backwards Compatibility with I2C**_ `43` _**Section 2.16: Address Assignment**_ `44` _**Section 2.17: In-Band Interrupt and Hot-Join**_ `45` _**Section 2.18: Common Command Codes (CCCs)**_ `46` _**Section 2.19: High Data Rate (HDR) Modes**_ `47` _**Section 2.20: I3C Advanced Capabilities**_ `48` _**Section 2.21: Electricals and Signaling**_ `49` _**Section 2.22: Bus Conditions and States**_ `50` _**Section 2.23: Resets and Error Handling**_ `51` _**Section 2.24: Timing Parameters**_ 

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

FAQ for MIPI I3C v1.1.1 & MIPI I3C Basic v1.1.1 

FAQ Version 1.1 22-Aug-2022 

- `52` 

## **General Questions** 

## **2.1 Introduction to MIPI I3C** 

## **Q1.1 What is MIPI I3C and I3C Basic?** 

`53` MIPI I3C is a serial communication interface specification that improves upon the features, performance, `54` and power use of I²C, while maintaining backward compatibility for most devices. 

`55` MIPI I3C Basic is technically identical to MIPI I3C, except with a reduced feature set and RAND-Z licensing `56` (see _**Section 2.11**_ ). 

## **Q1.2 What does the I3C acronym mean?** 

- `57` The official name is _MIPI Alliance Improved Inter Integrated Circuit_ . 

## **Q1.3 Why is MIPI I3C being introduced?** 

## `58` 

The main purpose of MIPI I3C is threefold: 

- `59` 1. To standardize sensor communication, 

- `60` 2. To reduce the number of physical pins used in sensor system integration, and 

- `61` 3. To support low power, high speed, and other critical features that are currently covered by I²C and `62` SPI. 

- `63` MIPI I3C’s purpose is now widening to cover many types of devices currently using I²C/SMbus, SPI, and `64` UART. 

## **Q1.4 What are the main features of MIPI I3C?** 

`65` MIPI I3C carries the advantages of I²C in simplicity, low pin count, easy board design, and multi-drop (vs. `66` point-to-point), but provides the higher data rates, simpler pads, and lower power of SPI. I3C then adds higher `67` throughput for a given frequency, In-Band Interrupts (from Target to Controller), Dynamic Addressing, `68` advanced power management, and Hot-Join. 

## **Q1.5 For which applications or use cases is I3C intended to be used?** 

`69` I3C was initially intended for mobile applications as a single interface that can be used for all digitally `70` interfaced sensors. However, it is now intended for all mid-speed embedded and deeply-embedded `71` applications across sensors, actuators, power regulators, MCUs, FPGAs, etc. The interface is also useful for `72` other applications, as it offers high-speed data transfer at very low power levels while allowing multi-drop, `73` which is highly desirable for any embedded system. 

## **Q1.6 How can the MIPI I3C specifications be obtained?** 

- `74` • **MIPI I3C Specification :** MIPI Alliance members have access and rights to the _**MIPI I3C**_ `75` _**Specification**_ through their MIPI membership and member website. The latest adopted version is `76` MIPI I3C v1.1.1 _**[MIPI13]**_ . 

- `77` • **MIPI I3C Basic Specification:** MIPI Alliance made the _**MIPI I3C Basic v1.0 Specification**_ `78` _**[MIPI09]**_ publicly available for download in December 2018. The latest adopted version is MIPI `79` I3C Basic v1.1.1 _**[MIPI14]**_ . MIPI Alliance members have access and rights to the I3C Basic `80` specification through their MIPI membership and member website. 

- `81` • **Non-members may download** a copyright-only version of the I3C Basic specification by `82` visiting the MIPI I3C Basic page on the MIPI Alliance website: `83` https://www.mipi.org/specifications/i3c-sensor-specification. 

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

4 

FAQ Version 1.1 22-Aug-2022 

FAQ for MIPI I3C v1.1.1 & MIPI I3C Basic v1.1.1 

## **2.2 Migration from Legacy I[2] C or Other Buses** 

## **Q2.1 Why replace I[2] C with I3C?** 

- `84` While I[2] C has seen wide adoption over the years, it lacks some critical features – especially as mobile and `85` mobile-influenced systems continue to integrate more and more sensors and other components. I[2] `86` limitations worth mentioning include: 7-bit fixed address (no virtual addressing), no in-band interrupt `87` (requires additional wires/pins), limited data rate, and the ability of Targets to stretch the clock (thus `88` potentially hanging up the system, etc.). I3C aims both to fix these limitations, and to add other `89` enhancements. 

## **Q2.2 Does I3C use less power than I²C?** 

- `90` The power consumption per bit-transfer in all I3C modes is more efficient than I²C, due to the use of push-pull `91` (vs. Open-Drain) and strong Pull-Up signaling. 

- `92` Further, I3C can save considerable device power through higher data rates (because the device can be put `93` back to sleep sooner), built-in configuration and control (without intruding on the main communication `94` protocols), In-Band Interrupt (IBI) as a low-cost wake mechanism, and the ability for Targets to shut down `95` all internal clocks while still operating correctly on the I3C Bus. 

## **Q2.3 How is I3C different from I²C?** 

- `96` I3C offers dynamic address assignment, Target-initiated communication, and significantly higher `97` communication speeds than I²C. 

## **Q2.4 Why replace SPI (Serial Peripheral Interface) with I3C?** 

- `98` SPI requires four wires and has many different implementations because there is no clearly defined standard. `99` In addition SPI requires one additional chip select (or enable) wire for each additional device on the bus, 

- `100` which quickly becomes cost-prohibitive in terms of number of pins and wires, and power. I3C aims to fix `101` that, as it uses only two wires and is well defined. 

- `102` I3C covers most of the speed range of SPI, but is not intended for the highest speed grades that really only `103` work well with a point-to-point interface, such as for SPI Flash. 

## **2.3 I3C Versions and Releases** 

## **Q3.1 What is new in I3C v1.1?** 

- `104` MIPI I3C v1.1 is an advancement of the MIPI I3C Specification that includes not only clarifying edits to `105` make for a more easily-implemented interface, but also new optional features that make I3C even more `106` attractive to a broader set of use cases and industries. 

- `107` The new features include: 

- `108` • HDR-BT (Bulk Transport) Mode 

- `109` • Device to Device(s) Tunneling 

- `110` • Grouped Addressing 

- `111` • Multi-Lane for Speed 

- `112` • Target Reset 

- `113` Additionally, many clarifying edits have been made to the specification, and the GETHDRCAPS CCC has `114` been replaced with the GETCAPS CCC (which is required for I3C v1.1 Devices). 

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

FAQ for MIPI I3C v1.1.1 & MIPI I3C Basic v1.1.1 

FAQ Version 1.1 22-Aug-2022 

## **Q3.2 What are the required features in I3C v1.1 vs. I3C 1.0?** 

`115` Almost all new features of I3C v1.1 are optional. 

- `116` However, it should be noted that: 

- `117` • The formerly optional CCC GETHDRCAPS has been changed to GETCAPS, and its support is `118` required for I3C v1.1 Devices, so as to indicate it is a v1.1 (or later) Device. 

- `119` • Additionally, it is necessary to support the new RSTACT CCC; as a result, support for a minimal `120` Target Reset is required. 

`121` MIPI recommends that Targets consider support of improvement features (such as Flow control for HDR, `122` and Group Addressing), as well as features they likely could use for their application. 

## **Q3.3 Are there any I3C v1.0 features that are not supported in I3C v1.1 and beyond?** 

`123` The Directed form of the RSTDAA CCC is not supported in I3C v1.1 and beyond. 

## **Q3.4 What is new in MIPI I3C v1.1.1?** 

`124` MIPI I3C v1.1.1 is an editorial update of MIPI I3C v1.1 that contains no new features or capabilities, but `125` resolves issues, clarifies, and improves on the I3C v1.1 specification. 

`126` MIPI I3C v1.1.1 includes: 

- `127` • Fixes for inconsistencies and other issues that were technical errors in MIPI I3C v1.1 (including `128` all issues resolved by Errata 01) 

- `129` • Clarifications to the requirements and procedures used for Dynamic Address Assignment, Hot- `130` Join Requests and In-Band Interrupts 

- `131` • Clarifications to Target Error Types TE0, TE5, and TE6 

- `132` • Improved clarity and fixes for issues in the sections that define CCC flows in HDR Modes `133` (generic as well as HDR Mode–specific) 

- `134` • Additional clarifications and explanations in some sections that did not fully explain new features `135` and capabilities introduced with I3C v1.1 

- `136` • Better explanations of I3C Devices that support advanced features, such as composite I3C Devices `137` that present multiple I3C Target roles (i.e., Virtual Targets) 

- `138` • Additional clarifications concerning the intersection of several of these new features and `139` capabilities when implemented together (i.e., when used in concert in the same I3C Bus with I3C `140` Devices that choose to support several or all such features or capabilities concurrently) 

- `141` • Limited allowances for flexibility in how certain new features and capabilities could be applied, or `142` which of these new features and capabilities might be regarded as required, optional, or `143` conditionally required per use case 

- `144` • Improved descriptions for Multi-Lane Device configuration, including clarified requirements for `145` I3C Devices that present multiple Dynamic Addresses and/or support Group Addressing 

- `146` • Additional diagrams for HDR-BT Mode, including the 1-Lane forms of the structured protocol `147` elements (i.e., Blocks) that are used in HDR-BT transfers, as well as an example of an HDR-BT `148` transfer 

- `149` • Improved descriptions of error detection and recovery methods, such as Error Type TE0 and Error `150` Type DBR (Dead Bus Recovery) 

- `151` • Changes to the Multi-Lane signaling of the Header Byte in SDR Mode 

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

6 

FAQ Version 1.1 22-Aug-2022 

FAQ for MIPI I3C v1.1.1 & MIPI I3C Basic v1.1.1 

## **Q3.5 Is I3C v1.1.1 compatible/interoperable with I3C v1.1?** 

- `152` Yes. I3C v1.1.1 is a purely editorial update that aims to resolve inconsistencies and improve clarity compared `153` to I3C v1.1; no new features or capabilities are added. I3C v1.1.1 addresses all I3C v1.1 issues that Errata 01 `154` did. Implementers are strongly advised to confirm that any I3C v1.1–compliant Devices adhere to the fixes `155` published in Errata 01. 

- `156` In particular, see _**Q4.4**_ for fixed issues regarding HDR-DDR Mode inconsistencies pertaining to zero-HDR- 

`157` DDR-Data-Word flows, which are no longer allowed. This affects all HDR-DDR transactions, including CCC `158` flows in HDR-DDR Mode. 

## **Q3.6 What is new in I3C Basic v1.1.1?** 

- `159` I3C Basic v1.1.1 is a fundamental update to I3C Basic v1.0, and adds many of the new optional capabilities `160` from I3C v1.1. I3C Basic v1.1.1 also includes clarifications and fixes for issues that were addressed in I3C `161` v1.1.1 (see _**Q3.4**_ ). Devices that comply with I3C Basic v1.1.1 should be mutually interoperable with I3C `162` v1.1.1, and vice versa. 

- `163` I3C Basic v1.1.1 is a subset of I3C v1.1.1, and adds the following features and capabilities: 

- `164` • HDR-DDR Mode 

- `165` • HDR-BT (Bulk Transport) Mode 

- `166` • Grouped Addressing 

- `167` • Multi-Lane for Speed (for HDR-BT Mode only) 

- `168` • Target Reset with RSTACT CCC (previously defined in a separate addendum for I3C Basic v1.0) 

- `169` • Timing Control (Async Mode 0 only) 

- `170` • CCCs in HDR Modes 

- `171` • GETCAPS CCC 

- `172` • SETBUSCON CCC 

- `173` • SETROUTE CCC 

- `174` • Virtual Target support 

`175` I3C Basic v1.1.1 also includes numerous clarifications and improved definitions, including Secondary `176` Controllers, Hot-Join, Dynamic Address Assignment, Target Error Types and FSM diagrams. 

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

FAQ for MIPI I3C v1.1.1 & MIPI I3C Basic v1.1.1 

FAQ Version 1.1 22-Aug-2022 

## **2.4 Up and Coming** 

## **Q4.1 What future MIPI specifications will be leveraging I3C?** 

`177` Many other MIPI Alliance Working Groups are in the process of leveraging the I3C specification. As of the `178` writing of this FAQ, the list includes: 

- `179` • **Camera WG:** Camera Control Interface (CCI) chapter of the _**MIPI Specification for Camera**_ `180` _**Serial Interface 2 (CSI-2), v4.0 [MIPI06]**_ (In development) 

- `181` 

- **Debug WG:** _**MIPI Specification for Debug for I3C, v1.1 [MIPI15]**_ (In development) 

## **Q4.2 Are there any impending fixes or errata for MIPI I3C v1.0 or I3C Basic v1.0 that should be applied now?** 

`182` _**Note:**_ 

- `183` _With the release of I3C v1.1 this question has been deprecated; it is retained here for reference._ `184` _See_ _**Q3.1** for what’s new in I3C v1.1._ 

- `185` All fixes or Errata for I3C v1.0 have also been applied to I3C v1.1. However, I3C v1.1 has since been `186` superseded by MIPI I3C v1.1.1, which is the newest recommended version of the I3C specification. 

- `187` All fixes for Errata for I3C Basic v1.0 have been incorporated into I3C Basic v1.1.1, which is the newest `188` recommended version of the I3C Basic specification. 

`189` Based on learning from early implementations, I3C Interoperability Workshops, queries from adopters, and `190` reviews by the I3C WG, this FAQ represents clarifications, improvements that can be implemented by I3C `191` v1.0 Devices or I3C Basic v1.0 Devices, and other guidance for implementers. 

## **Q4.3 Are any revisions to MIPI I3C v1.0 expected?** 

`192` No, there are no pending updates at this time. However, MIPI Alliance strongly recommends that all `193` implementers move to MIPI I3C v1.1.1 as the newest recommended version of the I3C specification. 

## **Q4.4 Are there any impending fixes or errata for MIPI I3C v1.1 that should be applied now?** 

`194` Yes, several fixes to MIPI I3C v1.1 have been identified, and MIPI has published these fixes as Errata 01. `195` These fixes fall into four categories: 

- `196` **1. Resolving inconsistencies in HDR-DDR Mode** 

- `197` I3C v1.0 and v1.1 did not consistently describe whether an HDR-DDR Data Word was always `198` required for HDR-DDR transactions. Additionally, I3C v1.1 introduced CCC flows in HDR-DDR `199` Mode, which assumed that flows with zero HDR-DDR Data Words were both possible and valid, `200` and it did not always provide appropriate acknowledgement for Target Devices. 

- `201` Errata 01 resolves these inconsistencies by always requiring at least one HDR-DDR Data Word for `202` all HDR-DDR transactions. Furthermore, Errata 01 clarifies the requirements for CCC flows in `203` HDR-DDR Mode, and re-defines the special use of the structured protocol elements for these CCC `204` flows to always include at least one HDR-DDR Data Word for appropriate acknowledgement. 

## `205` **2. Clarifying Open-Drain timing parameters** 

- `206` The timing parameters for I3C v1.1 did not show appropriate definitions for a ‘Pure Bus’ `207` configuration, and also did not provide clarity for sending the first I3C Address Header with the `208` Broadcast Address (i.e., 7’h7E) in order to disable the I[2] C Spike Filter (for certain I3C Devices). 

- `209` Errata 01 clarifies these timing parameters and fixes other related incorrect timing parameter `210` definitions. 

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

8 

FAQ Version 1.1 22-Aug-2022 

FAQ for MIPI I3C v1.1.1 & MIPI I3C Basic v1.1.1 

- `211` **3. Updating obsolete FSM Diagrams** 

- `212` Several FSM diagrams in Annex C that were initially created during early stages of I3C v1.0 `213` specification development were obsolete. For example, the FSM diagram for Dynamic Address `214` Assignment did not reflect the correct Dynamic Address Assignment procedure, and did not `215` include newer CCCs (such as the SETAASA CCC) that were added after I3C v1.0. Several other `216` issues and inconsistencies were also found in other FSM diagrams in Annex C. 

- `217` Errata 01 updates these FSM diagrams to reflect the correct procedures (per the normative text in `218` the I3C v1.1 specification) and to remove other obsolete terminology. 

- `219` **4. Typographical fix regarding HDR-TSP and Multi-Lane support** 

- `220` Errata 01 corrects a minor typographical error, and resolves an inconsistency regarding which `221` HDR Modes support Multi-Lane transfers in I3C v1.1. 

- `222` Additionally, these issues, plus numerous other inconsistencies, clarifications, and fixes have been addressed 

- `223` in MIPI I3C v1.1.1 _**[MIPI13]**_ . MIPI Alliance strongly recommends that all implementers move to MIPI I3C `224` v1.1.1 as the newest recommended version of the I3C specification. 

## **Q4.5 Are any revisions to I3C v1.1 expected?** 

- `225` MIPI I3C v1.1.1 addresses all issues found in I3C v1.1, including those that were published as Errata 01. `226` MIPI Alliance strongly recommends that all implementers move to MIPI I3C v1.1.1 as the newest `227` recommended version of the I3C specification. 

## **Q4.6 Are any revisions to I3C v1.1.1 expected?** 

- `228` Not at this time. However, the MIPI I3C WG meets regularly and is considering proposals to revise and `229` extend I3C. As part of maintaining the I3C specification, the MIPI I3C WG seeks to improve the I3C `230` specification in areas where it would benefit from clarification or additional explanation. Please direct any `231` comments or suggestions to MIPI Alliance. 

## **Q4.7 Are there any impending fixes or errata for I3C v1.1.1 and I3C Basic v1.1.1 that should be applied now?** 

- `232` Yes, several fixes to the MIPI I3C v1.1.1 and I3C Basic v1.1.1 specifications have been identified. MIPI has `233` published some of these in Errata 01 for I3C v1.1.1, and is currently working to publish others. `234` These fixes fall into four categories: 

- `235` **1. Clarifying requirements for Passive Hot-Join** 

- `236` A key technical detail was omitted in I3C v1.1.1 and I3C Basic v1.1.1: a passive Hot-Joining `237` Target needs to see an SDR Frame that is addressed to the Broadcast Address (i.e., 7’h7E / W) in `238` order to determine that it is indeed on an I3C Bus (see _**Q17.7**_ ). Additionally, once it sees this SDR `239` Frame, a passive Hot-Joining Target may either (a) pull SDA Low to raise its own Hot-Join `240` Request, or (b) wait for another I3C Device to pull SDA Low and then arbitrate the Hot-Join `241` Address (i.e., 7’h02) into the Arbitrable Address Header. 

- `242` _**Note:**_ 

- `243` _The I3C v1.1 specification did note the correct requirement for the Broadcast Address._ 

- `244` **2. Clarifying requirements for RSTACT Direct CCC read values** 

- `245` In I3C v1.1.1 and I3C Basic v1.1.1, the RSTACT Direct CCC with valid Defining Bytes for `246` different Target Reset operations (i.e., Defining Bytes 0x00 through 0x03) should return the last `247` configured Defining Byte accepted by the Target (unless no RSTACT CCC had previously been `248` used, in which case the defined read value was 0x00). However, implementers discovered that the `249` default read value of 0x00 was not distinguishable from the state when Defining Byte 0x00 had `250` been previously written by the RSTACT CCC (i.e., either Direct Write, or Broadcast use of `251` Defining Byte 0x00 to take no reset action on the Target Reset Pattern, per _**Table 53**_ ). This meant `252` that value 0x00 was not mapped to a single clear state of an unconfigured Target, and this caused `253` ambiguity. 

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

FAQ for MIPI I3C v1.1.1 & MIPI I3C Basic v1.1.1 

FAQ Version 1.1 22-Aug-2022 

- `254` Additionally, since the default action for an I3C Target to take after a Target Reset Pattern with no `255` preceding RSTACT CCC(s) is a reset of the I3C Peripheral, the default read value of 0x00 did not `256` accurately reflect an unconfigured state or the default action that would be taken. The new default `257` read value for the RSTACT Direct CCC with valid Defining Bytes has been changed to 0x80, to `258` distinguish clearly from both (a) the unconfigured state (i.e., armed to reset the I3C Peripheral), `259` and (b) the state where the Target has accepted a previous RSTACT CCC with Defining Byte 0x00 `260` (i.e., take no reset action). 

- `261` **3. Clarifying requirements for Max Write Length (SETMWL/GETMWL) and Max Read Length** `262` **(SETMRL/GETMRL)** 

- `263` I3C v1.0 specified that the minimum value for SETMWL (Max Write Length) was 8 bytes. I3C `264` v1.1 and v1.1.1 changed this minimum value to 16 bytes. However, this caused confusion for `265` implementers. The minimum values for SETMWL and SETMWL are no longer defined, and `266` implementers may now choose which values for Max Write Length and Max Read Length to `267` support. (See also _**Q18.18**_ .) 

- `268` **4. Clarifying minimum timing parameters for the HDR Restart Pattern and Target Reset Pattern** 

- `269` I3C v1.1 and v1.1.1 did not explicitly define the minimum timing parameters that the Controller 

- `270` must use when sending either the HDR Restart Pattern or the Target Reset Pattern. Since both of `271` these patterns are based on the HDR Exit Pattern, it was implied that the minimum timing 

- `272` parameters for the HDR Exit Pattern also applied to these other patterns. This is now explicitly `273` defined for all such patterns, and the Controller shall observe the minimum timing as defined by `274` parameter **tDIG_H** for all transitions. (See also _**Q24.6**_ .) 

- `275` MIPI Alliance plans to address these issues by including these clarifications in the next update to the I3C and `276` I3C Basic specifications. 

- `277` _**Note:**_ 

- `278` _MIPI Alliance strongly recommends that all implementers use the latest version of the I3C_ `279` _specifications with the most current published Errata._ 

## **Q4.8 What new features, if any, are coming to MIPI I3C?** 

- `280` There are no new approved features, however the MIPI I3C WG is considering the following: 

- `281` • Automotive-focused capabilities 

- `282` • Security over I3C 

- `283` • Improved reliability 

- `284` • Speed increases 

- `285` • New Multi-Lane uses 

- `286` • Long Reach 

- `287` • New HDR Modes 

- `288` • Refining existing features 

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

10 

FAQ Version 1.1 22-Aug-2022 

FAQ for MIPI I3C v1.1.1 & MIPI I3C Basic v1.1.1 

## **2.5 Naming and Terminology** 

## **Q5.1 What is an I3C “Controller” Device, and why was the I3C “Master” Device renamed?** 

`289` As part of a terminology replacement effort across MIPI Alliance, starting with I3C v1.1.1 and I3C Basic `290` v1.1.1 the terms Master and Slave have been deprecated. An I3C v1.0/v1.1 Master Device is now called a `291` Controller. There is no change to the technical definition of such an I3C Device or its role on an I3C Bus. `292` The term Controller is a better, more accurate description of the Device’s role on an I3C Bus. 

- `293` Due to this change, the names of various CCCs and other, related terms have also changed starting with `294` v1.1.1, including: 

|his change, the names of various CCCs and<br>cluding:|other, related terms have also changed star|
|---|---|
|**Deprecated Prior Term**<br>_I3C and I3C Basic before v1.1.1_|**Replacement Term**<br>_I3C and I3C Basic v1.1.1 and Later_|
|Master|Controller|
|Current Master|Active Controller|
|Secondary Master|Secondary Controller|
|Main Master|Primary Controller|
|New Master (relating to Handoff)|New Active Controller|
|Master-capable Device|Controller-capable Device|
|Mastership, Mastering the Bus, etc.|Controller Role, Control of the Bus, etc.|
|Mastership Request|Controller Role Request|
|GETACCMST CCC|GETACCCR CCC|
|Error Types M0 through M3|Error Types CE0 through CE3|



- `295` See also _**Q5.2**_ . 

## **Q5.2 What is an I3C “Target” Device, and why was the I3C “Slave” Device renamed?** 

- `296` As part of a terminology replacement effort across MIPI Alliance, starting with I3C v1.1.1 and I3C Basic `297` v1.1.1 the terms Master and Slave have been deprecated. An I3C v1.0/v1.1 Slave Device is now called a `298` Target. There is no change to the technical definition of such an I3C Device or its role on an I3C Bus. 

`299` The term Target is a better, more accurate description of the Device’s role on an I3C Bus. In particular, the `300` previous term did not describe I3C transfers, which are typically sent by the I3C Controller to individual I3C `301` Devices or to all I3C Devices. The replacement term Target better describes how individual transfers are `302` addressed (i.e., are “targeted”) to particular I3C Devices. 

`303` Due to this change, the names of various CCCs and other, related terms have also changed starting with `304` v1.1.1, including: 

|his change, the names of various CCCs and<br>cluding:|other, related terms have also changed star|
|---|---|
|**Deprecated Prior Term**<br>_I3C and I3C Basic before v1.1.1_|**Replacement Term**<br>_I3C and I3C Basic v1.1.1 and Later_|
|Slave|Target|
|Slave Reset Pattern|Target Reset Pattern|
|DEFSLVS CCC|DEFTGTS CCC|
|Error Types S0 through S6|Error Types TE0 through TE6|



`305` See also _**Q5.1**_ . 

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

11 

FAQ for MIPI I3C v1.1.1 & MIPI I3C Basic v1.1.1 

FAQ Version 1.1 22-Aug-2022 

```
309
310
```

```
311
```

```
312
```

## **2.6 Implementation: Ecosystem** 

## **Q6.1 Who is defining the MIPI I3C Specifications?** 

`306` The I3C specification is defined by the MIPI Alliance I3C Working Group (originally named the Sensor `307` Working Group) which was formed in 2013. I3C Basic is defined by the MIPI Alliance I3C Basic Ad-Hoc `308` Working Group which was formed in 2018. 

## **Q6.2 Is anyone currently using I3C?** 

Yes, a number of companies have released products that feature integrated I3C Controller and I3C Target support. Other companies offer IP blocks and associated verification software for adding I3C Bus support into various integrated circuit designs. Some companies also offer protocol analyzers and verification hardware to help analyze I3C Bus traffic for testing and development. 

- `313` 

```
314
```

Since this document cannot provide a comprehensive list of such products, those who are interested in learning more about products that support or enable I3C should contact MIPI Alliance. 

## **Q6.3 What is the availability of development hardware for I3C prototyping, including FPGAs?** 

`315` Several vendors have provided FPGA based design kits, including some low-cost FPGAs that might be good `316` enough for smaller production runs. 

## **Q6.4 What is the I3C IP core availability in the market?** 

`317` Some vendors have started to offer Target and/or Controller IP cores for integration into ASIC devices and `318` FPGAs, including a free-of-cost Target IP available for prototyping and integration. 

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

12 

FAQ Version 1.1 22-Aug-2022 

FAQ for MIPI I3C v1.1.1 & MIPI I3C Basic v1.1.1 

## **2.7 Implementation: As a System Designer** 

## **Q7.1 What is the maximum capacitance load allowed on the I3C Bus?** 

`319` The I3C specification lists the maximum per-Device capacitance on SCL and SDA, but the goal is that most `320` or all Devices will be well below that. As with any Bus, capacitance alone is not sufficient to determine `321` maximum frequency on the I3C Bus. It is important to consider maximum propagation length, effect of stubs, `322` internal clock-to-data (tSCO) of the Targets, as well as capacitive load. 

## **Q7.2 What is the maximum wire length for I3C communication?** 

- `323` 

- `324` 

- `325` 

- `326` 

The maximum wire length would be a function of speed, as all the reflections and Bus turnaround must complete within one cycle. Larger distances can be achieved at the lower speeds than at the higher ones. For example, at 1 meter (between Controller and Target), the maximum effective speed is around 6 MHz for read, to allow for clock propagation time to Target and SDA return time to Controller. 

## **Q7.3 Can I[2] C repeaters be used for I3C?** 

- `327` 

- `328` 

Not directly, for a couple of reasons: 

   1. The I3C Bus works with push-pull modes (in addition to the open drain for some transfers), and 

- `329` 2. Much higher speeds. Most such devices are quite limited in speed, because of the lag effect of `330` changing states on SCL and SDA due to both series-resistance and assumptions about Open-Drain. 

- `331` Long wire approaches are being evaluated for a future version of the I3C specification. 

## **Q7.4 Will the I[2] C devices respond to I3C commands?** 

`332` No. The I3C CCCs are always preceded by the I3C Broadcast Address, 7’h7E. Since the I[2] C specification `333` reserves address 7’h7E, no Legacy I[2] C Target will match the I3C Broadcast Address, and thus no Legacy I[2] `334` Target would respond to the I3C commands. Likewise, the Dynamic Addresses assigned to I3C Devices `335` would not overlap the I[2] C static addresses, so no I[2] C device would respond to any I3C address – even if it `336` could see it. 

## **Q7.5 How are communication conflicts resolved on the I3C Bus?** 

`337` I3C Targets are only allowed to drive the Bus under certain situations. Besides during a read, and when `338` ACKing their own address, I3C Targets may also drive after a START (but not Repeated START). After a `339` START, the I3C Bus reverts back to Open-Drain Pull-Up resistor mode; thus, the Target that drives a low `340` value (i.e., logic 0) would win. 

## **Q7.6 Can I3C Devices cause the communication Bus to hang?** 

`341` Unlike I²C, there is no natural way to hang the I3C Bus. In I²C, clock stretching (where the Target holds the `342` clock low, stopping it from operating) often causes serious problems with no fix: there’s simply no way to `343` get the Target’s attention if it has hung the Bus. By contrast, in I3C only the Controller drives the clock, and `344` so the Target performs all actions on SDA relative to that clock, thereby eliminating the normal causes of `345` such hangs. 

`346` Further, since I3C is designed to ensure that I3C Targets can operate their back-end I3C peripheral off the `347` SCL clock (vs. oversampling), any problems elsewhere in the Target won’t translate into Bus hangs. 

`348` If a system implementer is highly concerned about a Target accidently locking itself, then a separate `349` hard-reset line could be used. Alternatively, the I3C v1.1.1 and I3C Basic v1.1.1 specifications add a new `350` feature called Target Reset for resetting non-responsive I3C Targets: if an I3C Controller emits the Target `351` Reset Pattern (a defined unique Bus pattern that does not otherwise occur during regular communication), `352` then the Devices on the Bus will treat it just like a hardwired reset line. 

- `353` 

- This question has been updated for I3C v1.1.1 and I3C Basic v1.1.1. 

## **Q7.7 Will all I3C Devices be compatible with all CCCs?** 

`354` No. Some CCCs are mandatory, whereas others are optional or conditionally supported, and a given I3C `355` Device will either support them or not, depending upon the Device’s capabilities. See also _**Q14.2**_ and _**Q18.7**_ 

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

13 

FAQ for MIPI I3C v1.1.1 & MIPI I3C Basic v1.1.1 

FAQ Version 1.1 22-Aug-2022 

## **2.8 Implementation: As a Software Developer** 

## **Q8.1 Are there any companion MIPI I3C Specifications that enable software development?** 

- `356` Yes. The following MIPI specifications are expected to help with software development: 

- `357` • _**MIPI Specification for I3C Host Controller Interface (I3C HCI), v1.0 [MIPI02]**_ `358` and 

`359` _**MIPI Specification for I3C Host Controller Interface (I3C HCI), v1.1 [MIPI12]**_ 

`360` Creates a standard definition that allows a single OS driver (also known as ‘in-box driver’) to `361` support I3C hardware from several vendors, while also allowing vendor-specific extensions or `362` improvements. The target audience of the HCI specification is application processor host 

- `363` controllers; in particular, developers of host controller (i.e., I3C Primary Controller) hardware, and `364` developers of I3C host controller software. 

`365` • _**MIPI Specification for Discovery and Configuration (DisCo), v1.0 [MIPI03]**_ `366` Describes a standardized device discovery and configuration mechanism for interfaces based on `367` MIPI specifications, which can simplify component design and system integration. Also oriented `368` to application processors. 

- `369` • _**MIPI DisCo Specification for I3C, v1.0 [MIPI04]**_ 

`370` Allows operating system software to use ACPI (Advanced Configuration and Power Interface) `371` structures to discover and configure the I3C host controller and attached I3C Devices in `372` ACPI-compliant systems. Also oriented to application processors. 

`373` In addition to these MIPI specifications, a supporting document is also available. The _**I3C Application Note:**_ `374` _**General Topics, App Note v1.1 [MIPI05]**_ has been developed to help ASIC hardware developers, system `375` designers, and others working in the more deeply embedded I3C Devices. The I3C WG plans to develop `376` additional Application Notes that will cover new features and capabilities included in I3C v1.1.1 and I3C `377` Basic v1.1.1. 

## **Q8.2 Are there software libraries available for I3C?** 

`378` Yes. Core I3C infrastructure has been added to the Linux Kernel as part of the I3C subsystem. The I3C `379` subsystem also includes drivers for several I3C Controller devices and IP core implementations, including `380` MIPI I3C HCI–compliant Host Controllers (see _**[MIPI12]**_ ). 

`381` The current list of Linux Kernel Patches for the I3C subsystem can be accessed via _**[LINX01]**_ . 

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

14 

FAQ Version 1.1 22-Aug-2022 

FAQ for MIPI I3C v1.1.1 & MIPI I3C Basic v1.1.1 

## **2.9 Interoperability Workshops** 

## **Q9.1 What is a MIPI I3C Interoperability Workshop?** 

`382` It is a MIPI Alliance sponsored event where different vendors bring their I3C implementations and check `383` interoperation with other vendors. 

## **Q9.2 What is the output from a MIPI I3C Interoperability Workshop?** 

`384` There are three major outputs from a MIPI I3C Interoperability Workshop: 

- `385` • Participating vendors can get detailed information about how well their I3C implementations `386` interoperate with other vendors’ implementation. Vendors can also compare their results with one `387` another. 

- `388` • MIPI Alliance can generate an overall picture of the industry state-of-the-I3C-implementaion. For `389` example, how many vendors have implemented I3C, and how many implementations pass or fail `390` against one another. 

- `391` • The MIPI I3C Working Group gets better understanding about any major issues with the I3C `392` specification. The WG can then leverage that learning by adding to this FAQ, other supporting `393` documents (such as Application Notes, per Q8.1), and possible future revision of MIPI I3C `394` specifications. 

## **Q9.3 Are MIPI I3C Interoperability Workshops an ongoing activity?** 

`395` MIPI arranges a particular I3C Interoperability Workshop event in response to requests from its membership. `396` They have typically been co-located with regularly scheduled MIPI Member Meetings. 

## **Q9.4 Who can attend or participate in a MIPI I3C Interoperability Workshop?** 

`397` In general, any MIPI Alliance members who have I3C hardware ready to interop can participate. 

## **Q9.5 What HW/SW is typically needed to participate in a MIPI I3C Interoperability Workshop?** 

`398` While this could change in future, the minimal requirements to date have been the availability of a board `399` with an I3C Device that can connect to other Devices via the three wires SDA, SCL, and GND. It’s also `400` useful to have software (e.g., running on a laptop connected to the board and I3C Device) to interactively `401` view transmitted and received Bus communications, but this might not be required for Targets. 

```
402
```

Currently there are solutions working at 3.3V and 1.8V. 

## **Q9.6 Are there any I3C Interoperability Workshops planned for I3C v1.1.1 or I3C Basic v1.1.1?** 

`403` MIPI Alliance has been hosting I3C Interoperability Workshops in conjunction with MIPI Member Meetings, `404` typically two to three times per year. At this time this FAQ was last updated (August 2022), in-person MIPI `405` Member Meetings have been suspended due to the pandemic. However, MIPI Alliance expects to schedule `406` I3C Interoperability Workshops once in-person MIPI Member Meetings resume. 

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

15 

FAQ for MIPI I3C v1.1.1 & MIPI I3C Basic v1.1.1 

FAQ Version 1.1 22-Aug-2022 

## **2.10 Conformance Testing** 

## **Q10.1 What is a MIPI Conformance Test Suite (CTS)?** 

- `407` A MIPI WG develops a Conformance Test Suite (CTS) document in order to improve the interoperability of `408` products that implement a given MIPI interface specification. The CTS defines a set of conformance or `409` interoperability tests whereby a product can be tested against other implementations of the same specification. 

## **Q10.2 Is there a MIPI CTS for I3C?** 

- `410` Yes, MIPI Alliance has released a CTS for I3C v1.1.1 and I3C Basic v1.1.1 _**[MIPI08]**_ . 

## **Q10.3 What is the scope of tests for the I3C CTS?** 

- `411` The CTS tests are designed to determine whether a given product conforms to a subset of the common I3C `412` requirements defined in both I3C v1.1.1 and I3C Basic v1.1.1 (i.e., the requirements that are common to both `413` specifications, since I3C Basic is a subset of I3C). The scope of this version of the CTS is intentionally `414` limited, in order to meet time-to-market requirements imposed by the rapid adoption of I3C in the `415` marketplace, focusing on: 

- `416` 1. SDR-only Devices without optional I3C capabilities, 

- `417` 2. All Controller and Target Error Detection and Recovery methods, and 

- `418` 3. Basic HDR Enter/tolerance/Restart/Exit procedures. However, specific HDR Modes are not `419` covered by this version of the CTS. 

- `420` Considering the CTS a living document, the I3C WG plans to continue expanding the scope of the CTS `421` through future revisions or subordinate CTS documents for specific features or capabilities (e.g., HDR `422` Modes). The growing set of CTS documents should eventually encompass a broad array of all required and `423` optional features of both the I3C specification and the I3C Basic specification. 

`424` The CTS tests are organized as Controller DUT tests (Device Under Test) and Target DUT tests. Tests for `425` each are presented in the order in which they appear in the I3C specification, to simplify identification of `426` pertinent detail between the two documents. 

## **Q10.4 Does the I3C Interoperability Workshop follow the I3C CTS?** 

- `427` Interoperability Workshops will ultimately follow the tests identified in the I3C CTS, as and when such events `428` can be arranged by MIPI Alliance. 

## **Q10.5 What details are provided for each I3C CTS test case?** 

`429` Each test in the I3C CTS contains: 

- `430` • A clear purpose 

- `431` • References 

- `432` • Resource requirements 

- `433` • Tracked last technical modification 

- `434` • Discussion 

- `435` • All test case detail (i.e., Setup, Procedure, Results, and Problems). 

`436` DC/AC parametric requirements are embedded in each test (not split out into a separate PHY-related CTS or `437` subsection). 

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

16 

FAQ Version 1.1 22-Aug-2022 

FAQ for MIPI I3C v1.1.1 & MIPI I3C Basic v1.1.1 

## **2.11 Legal and Intellectual Property Related Questions** 

## **Q11.1 Is MIPI I3C Basic royalty free?** 

- `438` The parties that directly developed the MIPI I3C Basic specification have agreed to license all implementers `439` on royalty free terms, as further described in the I3C Basic specification document _**[MIPI09][MIPI14]**_ `440` Further, all implementers of the I3C Basic specification must commit to grant a reciprocal royalty free license `441` to all other implementers if they wish to benefit from these royalty free license commitments. And, of course, `442` MIPI itself does not charge royalties in connection with its specifications. MIPI’s intent is to create a robust `443` royalty free environment for all implementers of I3C Basic. 

- `444` No set of IPR terms can comprehensively address all potential risks, however. The terms apply only to those `445` parties that agree to them, for example, and the scope of application is limited to what is described in the `446` terms. Implementers must ultimately make their own risk assessment. 

## **Q11.2 What license terms apply to MIPI I3C v1.x?** 

`447` MIPI’s regular IPR terms apply to the full MIPI I3C specification. MIPI’s terms require that members make `448` licenses available only to other members, as described in the MIPI Membership Agreement and MIPI Bylaws. `449` To benefit from the license commitments, a party must be a MIPI member. 

- `450` For features that are included in MIPI I3C Basic, a MIPI member can implement under the regular IPR terms, `451` or can opt to implement the feature under the I3C Basic framework. If a member opts in to the I3C Basic `452` framework, then they must grant the reciprocal licenses required under that framework. MIPI Alliance `453` members are not required to participate in the I3C Basic license framework, however. Features of I3C 1.x `454` that are not included in I3C Basic are subject only to MIPI’s regular IPR terms. 

`455` Prior to the release of I3C Basic, MIPI had made certain versions of the full MIPI I3C specification available `456` for public review, under “copyright only” terms – that is, MIPI published the specification, but noted that no `457` rights to implement the specification were granted under any party’s patent rights. MIPI no longer publishes `458` the full I3C specification publicly. A non-member is not granted any right to implement the full MIPI I3C 1.x `459` specification, either by MIPI or any MIPI member. 

- `460` 

I3C Basic is available to non-members, as described in _**Q1.6**_ . 

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

17 

FAQ for MIPI I3C v1.1.1 & MIPI I3C Basic v1.1.1 

FAQ Version 1.1 22-Aug-2022 

## `461` **Detailed Technical Questions** 

## **2.12 New Capabilities in I3C** 

## **Q12.1 Can I3C Targets initiate communication (i.e., interrupt the Controller)?** 

`462` Yes, I3C Targets can initiate communication using In-Band Interrupt requests. Communication conflicts are `463` solved by Target Address Arbitration. 

## **Q12.2 How can Controllers and Targets communicate on the I3C Bus?** 

`464` The basic byte-based messaging schemes used in I²C and SPI map easily onto I3C. Additionally, a set of `465` Common Command Codes (CCCs) has been defined for standard operations like enabling and disabling `466` events, managing I3C-specific features (e.g., Dynamic Addressing, Timing Control), and other functions. `467` CCCs are either Broadcasted (i.e., sent to all Devices on the I3C Bus), or else Directed to a particular Device `468` on the I3C Bus (i.e., by Address). 

- `469` CCCs do not interfere with, and do not consume any of the message space of, normal Controller-to-Target `470` communications. That is, I3C provides a separate namespace for CCCs (see the specification at `471` _**Section 5.1.9.3**_ ). 

## **Q12.3 What are CCCs (Common Command Codes) and why are they used?** 

`472` CCCs are the commands that an I3C Controller uses to communicate to some or all of the Targets on the I3C `473` Bus. The CCCs are sent to the I3C Broadcast address (which is 7’h7E) so as not to interfere with normal `474` messages sent to a Target. In other words, CCCs are separated from the standard “content protocol” used by `475` normal messages, such as Private Write and Read transfers (in SDR Mode). 

`476` The CCCs are used for standard operations like enabling/disabling events, managing I3C-specific features, `477` and other Bus operations. CCCs can be either Broadcasted (i.e., sent to all Devices on the I3C Bus), or else `478` Directed to specific Devices on the I3C Bus (i.e., by Address). All CCC command number values are `479` allocated by MIPI Alliance, and some values are reserved for specific purposes including MIPI Alliance `480` enhancements and other extensions (see _**Q18.4**_ ). 

## **Q12.4 How are the following similar and/or different: In-Band Interrupt, Hot-Join, and Controller Role Request (IBI / HJ / CRR)?** 

- `481` All three are special, in-band methods that allow the Target to notify the Controller of a new request or state, `482` without having to wait for the Controller to query or poll the Target(s). The term ‘in-band’ refers to doing `483` this via the I3C Bus wires/pins themselves, rather than using methods requiring extra wires/pins. 

- `484` • **In-Band Interrupt (IBI):** A Target uses an IBI Request to notify the Controller of a new state or `485` event. If the Target so indicates in the BCR, then an IBI may include one or more following data `486` bytes. A Target can only use IBI if it has indicated the intent to do in its BCR. 

- `487` If the Target indicates it will send data with an IBI, then it is required to always send at least 1 `488` byte, called the Mandatory Data Byte (MDB). Starting with I3C v1.1, the MDB is coded following `489` certain rules. Any data after the MDB is a contract between Controller and Target. 

- `490` • **Hot-Join (HJ):** A Hot-Join Request is used only by an I3C Target that hasn’t yet been assigned a `491` Dynamic Address and is attached or awakened on the I3C Bus after the Primary Controller has `492` initialized it. The Hot-Join Request uses a fixed address which is reserved for this purpose only. `493` The Controller will recognize this fixed address and then initiate a new Dynamic Address `494` Assignment procedure. However, a Target cannot use the Hot-Join Request before verifying that `495` the I3C Bus is in SDR Mode. 

- `496` • **Controller Role Request (CRR):** A Secondary Controller (including the Primary Controller, once `497` it has given up the Controller Role) sends a CRR when it wants to become Controller of the I3C `498` Bus. If the Active Controller accepts the CRR, then it will issue a GETACCCR CCC to pass the `499` Controller Role to the requesting Secondary Controller. It is also possible for the Active Controller 

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

18 

FAQ Version 1.1 22-Aug-2022 

FAQ for MIPI I3C v1.1.1 & MIPI I3C Basic v1.1.1 

`500` to initiate handoff on its own without any Target initiating an CRR, for example when a Secondary `501` Controller wants to return control. 

## **2.13 Limits and Performance** 

## **Q13.1 What is the maximum number of I3C Devices per Bus?** 

- `502` In I3C v1.1 and I3C Basic v1.0 the maximum number of I3C Target Devices was limited to 11. However, `503` this limit was calculated based on typical electrical parameters, whereas different system designs might `504` present other limitations or challenges. Also, the actual number of Targets presented on the Bus could be `505` higher if some of the I3C Devices enable Bridging (see _**Q20.3**_ ) or present Virtual Targets (see _**Q20.2**_ ) with `506` unique Dynamic Addresses. 

- `507` In I3C v1.1.1 and I3C Basic v1.1.1 the maximum number of I3C Target Devices is no longer stated as a fixed `508` number. Instead, system designers should determine a limit that satisfies all I3C electrical requirements (per `509` _**Section 6**_ ), based on the particular system’s unique layout and the unique selection of I3C Devices to be used `510` on the Bus. 

## **Q13.2 Can there be more than one I3C Target inside a chip?** 

`511` Yes, multi-Target I3C chips are possible. I3C v1.1 also defines Virtual Target capabilities; see _**Q20.2**_ for `512` examples of Virtual Targets. 

## **Q13.3 What is the bit rate for I3C?** 

- `513` I3C has several Modes, each with one or more associated bit rates. 

`514` The base raw bitrate for SDR Mode is 12.5 Mbps, with 11 Mbps real data rate at 12.5 MHz clock frequency. `515` This is the only Mode supported in both I3C v1.0 and I3C Basic v1.0. 

- `516` 

- `517` 

- `518` 

- `519` 

The maximum raw bitrate is 33.3 Mbps at 12.5 MHz, with real data rate of 30 Mbps. This is achieved via HDR Modes that are currently only available in I3C v1.x (i.e., not available in I3C Basic v1.0). 

Most traffic will use the 10–11 Mbps rate, while large messages can use one of the optional higher data rate (HDR) Modes or optional Multi-Lane transfers, which are available in I3C v1.1+ or I3C Basic v1.1.1. 

- `520` _**Note:**_ 

- `521` 

```
522
523
```

_This question was updated for I3C v1.1.1. The I3C Controller should use the GETCAPS CCC (formerly named GETHDRCAPS) to determine which optional HDR Modes are supported for a given I3C Target. For details, see the specification at_ _**Section 5.1.9.3.19** ._ 

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

19 

FAQ for MIPI I3C v1.1.1 & MIPI I3C Basic v1.1.1 

FAQ Version 1.1 22-Aug-2022 

## **Q13.4 Is it possible to have multiple Controllers on the same I3C Bus?** 

`524` Yes, I3C allows for multiple Controllers on the same Bus. However, only one Controller can have control of `525` the Bus (i.e., can possess the Controller Role) at any given time. 

`526` An I3C Bus has one Primary Controller that initially configures the Bus and acts as the initial Active `527` Controller. Optionally, the Bus can also have one or more Secondary Controller Devices; these initially act `528` as Targets, but any one of them can send the Active Controller a Controller Role Request (CRR) to ask to `529` take over the role of Active Controller. Once the Active Controller agrees to a CRR and transfers Bus control `530` (i.e., transfers the Controller Role) to a requesting Secondary Controller Device, the requesting Device then `531` becomes the new Active Controller. 

- `532` _**Note:**_ 

`533` _The previous Active Controller (including the Primary Controller) can attempt to regain Bus control_ `534` _by performing this same CRR process. Once the previous Active Controller passes the Controller_ `535` _Role to another Controller-capable Device, it typically acts as a Target (i.e., with limited scope) until_ `536` _it receives the Controller Role again. The terms Active Controller and Secondary Controller reflect_ `537` _the current role of the Device at any given time, not the Device’s initial configuration or capabilities._ `538` _See the specification at_ _**Section 5.1.7** for more details._ 

`539` If the Active Controller crashes or becomes unresponsive, then other Controller-capable Devices may use the `540` optional Error Type DBR procedure to test the Bus and regain control if necessary. For details, see the `541` specification at _**Section 5.1.10.1.8**_ . 

- `542` _**Note:**_ 

- `543` 

_This question was updated for I3C v1.1.1 and I3C Basic v1.1.1._ 

## **Q13.5 Can a Target indicate any speed limit that it might have?** 

`544` All I3C Targets must be tolerant of the 12.5 MHz maximum frequency, and all Targets must be able to manage `545` those speeds for CCCs. However, Targets may limit the maximum effective data rate for private messages – `546` either write, read, or both. 

## **Q13.6 Is there a maximum limit to I3C Bus payload length?** 

```
547
```

```
548
```

```
549
```

```
550
```

By default, there is no limit to the maximum message length. However, to reduce Bus availability latency across multiple Targets, the I3C Bus allows Controller and Target to negotiate for maximum message lengths. Further, the Controller can terminate a Read, which makes it possible to regain control of the Bus while in a long message. 

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

20 

FAQ Version 1.1 22-Aug-2022 

FAQ for MIPI I3C v1.1.1 & MIPI I3C Basic v1.1.1 

## **2.14 Minimum Required Features** 

## **Q14.1 Which features are required for a Device to be a compliant I3C Controller?** 

`551` A compliant I3C Device that can fulfill the Controller Role is required to: 

- `552` • Assign a unique Dynamic Address to any I3C Targets on the I3C Bus, using any combination of `553` the ENTDAA, SETDASA, and SETAASA CCCs that is appropriate for such I3C Targets. 

- `554` • Specification _**Section 5.1.4.2**_ defines the full requirements of the Dynamic Address Assignment `555` procedure. 

- `556` • The specific CCCs and known Static Addresses (if any) must be a prior configuration, i.e., `557` already known to the system designer. 

- `558` • Note that the SETAASA CCC was not defined in MIPI I3C v1.0, it was added in v1.1. 

- `559` • Manage its Pull-Up structures, including the Open Drain class Pull-Up and High-Keeper Pull-Up `560` for both SDA and SCL. Specification _**Section 5.1.3.1**_ defines the full requirements for these Pull- `561` Up structures; see also _**Q21.3**_ and _**Q21.4**_ . 

- `562` 

- `563` 

   - Manage START requests and Address Header arbitration in Open Drain mode. 

   - Recover I3C Target Devices using the Error Recovery Escalation Model (per _**Section 5.1.10**_ ). 

- `564` • Support all of the CCC commands that are mandatory for Controllers, including ENEC, DISEC, `565` ENTDAA, SETDASA, RSTDAA, GETCAPS, RSTACT, GETPID, GETBCR, GETDCR, and `566` GETSTATUS. 

- `567` _**Note:**_ 

- `568` _The requirements above apply to the I3C Device that is the Primary Controller of its I3C Bus (i.e., the_ `569` _first Active Controller). An I3C Device that is a Secondary Controller during Bus initialization (or one_ `570` _that subsequently joins after Bus initialization) does not need to meet all of these requirements. See_ `571` _specification_ _**Section 5.1.7** for specific requirements for I3C Buses with multiple Controller-capable_ `572` _Devices, including reduced-function Secondary Controllers._ 

## **Q14.2 Which features are required for a Device to be a compliant I3C Target?** 

`573` A compliant I3C Device that can fulfill the role of Target is required to: 

- `574` • Accept an assigned Dynamic Address from the Active Controller, using any or all of the supported `575` methods (i.e., ENTDAA, SETDASA, and/or SETAASA; see _**Q18.7**_ and specification _**Section**_ `576` _**5.1.4.2**_ ). Note that some of these methods require an I[2] C Static Address. 

- `577` • If the ENTDAA method is supported, then the Device must have a MIPI Provisional ID and a `578` MIPI-compliant DCR. 

- `579` • Detect when it is addressed by its assigned Dynamic Address in SDR Mode, and respond to any `580` I3C Private Read or Private Write transfers (as appropriate for the I3C content protocol). 

- `581` • Respond to the mandatory CCCs for Targets, including ENEC, DISEC, RSTDAA, GETCAPS, `582` GETSTATUS, and RSTACT 

- `583` • Note that other CCCs might also be conditionally required, such as GETPID, GETBCR, and (if `584` ENTDAA is supported) GETDCR. 

- `585` • Detect when the Active Controller enters any HDR Mode, using the ENTHDR0 – ENTHDR7 `586` CCCs, and either: 

- `587` • **If the Target supports that HDR Mode:** Monitor Bus activity according to the HDR Mode’s `588` signaling and coding, and respond appropriately to any HDR Read or HDR Write transfers that `589` are addressed to the Device’s Dynamic Address (or HDR Write transfers that are addressed to an `590` assigned Group Address, if applicable). 

```
591
```

   - Or: 

- `592` • **If the Target does not support that HDR Mode:** Ignore all activity on the Bus until the Target `593` sees the HDR Exit Pattern (per specification _**Section 5.2**_ and _**Section 5.2.1**_ ). 

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

21 

FAQ for MIPI I3C v1.1.1 & MIPI I3C Basic v1.1.1 

FAQ Version 1.1 22-Aug-2022 

- `594` • Implement Error detection and recovery methods for an I3C Target, including Error Types TE0 `595` through TE5 per specification _**Section 5.1.10**_ . 

## **2.15 Backwards Compatibility with I[2] C** 

## **Q15.1 Is I3C backward compatible with I²C?** 

- `596` Yes, most Legacy I²C Target devices can be operated on an I3C Bus, provided they have a 50 ns spike (glitch) `597` filter and do not attempt to stall the clock. Such use will not degrade the speed of communications to I3C `598` Targets; it will require decreased speed only when communicating with the I²C Targets. 

- `599` I3C supports Legacy I[2] C Target devices using Fast-mode (Fm, 400 KHz) and FastMode+ (Fm+, 1 MHz) with `600` the 50 ns spike filter, but not the other I[2] C modes, and not I[2] C devices lacking the spike filter, or I[2] C devices `601` that stretch the clock. 

## **Q15.2 Can I3C Devices operate on a Legacy I[2] C Bus?** 

- `602` I3C Target Devices that have a Static Address can operate as I[2] C Targets on an I[2] C bus; optionally, they can `603` also have a 50 ns spike filter. 

- `604` Additional requirements also apply; see also _**Q15.4**_ and the specification at _**Section 5.1.1.1**_ . 

## **Q15.3 Can I3C and I²C co-exist on the same bus?** 

- `605` Yes, both I3C and I²C can share the same bus, with some limitations: 

- `606` • I3C does not support Legacy I[2] C Controller Devices, because they cannot share the Bus with I3C `607` Devices. 

- `608` • I3C does support many Legacy I[2] C Target Devices, on the condition that they meet certain `609` guidelines; see also _**Q15.1**_ regarding backward compatibility. 

- `610` _**Note:**_ 

- `611` _This question has been updated for I3C v1.1.1 and I3C Basic v1.1.1._ 

## **Q15.4 How does an I3C Target behave with an I[2] C Controller vs. with an I3C Controller?** 

- `612` An I3C Target that supports both Legacy I[2] C and I3C buses typically initializes in I[2] C mode, as it does not `613` yet possess a Dynamic Address, and also might not know what type of bus is used. However, the Target `614` should be ready to receive a Dynamic Address from an I3C Controller. If the Target also has an I[2] C Static `615` Address, then it may operate on a Legacy I[2] C bus using that Static Address. An I3C Target may also support `616` an I[2] C 50 ns Spike Filter for I[2] C Fm and Fm+ modes, and it may support other I[2] C features that are not `617` supported by I3C (such as Device ID). However, per specification _**Section 5.1.1.1**_ , these features may only `618` be used on a Legacy I[2] C bus, never on an I3C Bus. 

- `619` For I3C Buses with such I3C Targets, the I3C Controller must emit the first I3C Address Header with the `620` Broadcast Address (7’h7E) at a rate that is slow enough to be seen through an I[2] C Spike Filter. This allows `621` such an I3C Target to disable its Spike Filter once it sees the first I3C Address Header with the Broadcast `622` Address (see _**Q24.1**_ and the specification at _**Section 5.1.2.1.1**_ ). 

- `623` If the I3C Target does not have an I[2] C Static Address, then it will simply wait for the first I3C Address Header `624` from an I3C Controller (i.e., an I3C Address Header containing the Broadcast Address). Such a Target would `625` be of no value on a Legacy I[2] C bus, since I[2] C relies on each Target having a Static Address. 

- `626` _**Note:**_ 

`627` _If such an I3C Target supports any Legacy I[2] C features that are not allowed on an I3C Bus (e.g.,_ `628` _clock stretching), then the implementer must ensure that these features are never used, unless the_ `629` _Target knows with certainty that it is on a Legacy I[2] C bus and not on an I3C Bus._ 

`630` _An I3C Target must not use clock stretching on an I3C Bus, since clock stretching is not allowed (see_ `631` _the specification at_ _**Section 5.1.1.1** ) and the SCL line is typically managed by the I3C Controller, and_ `632` _is driven in Push-Pull mode._ 

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

22 

FAQ Version 1.1 22-Aug-2022 

FAQ for MIPI I3C v1.1.1 & MIPI I3C Basic v1.1.1 

## **2.16 Address Assignment** 

## **Q16.1 Are all I3C Targets required to support Dynamic Address Assignment with the ENTDAA CCC?** 

- `633` No. If an I3C Target will only be used on I3C Buses that rely on the SETAASA CCC (a Broadcast CCC that `634` auto-sets the Target’s Dynamic Address from its I[2] C Static Address) and/or the SETDASA CCC (a Direct 

- `635` CCC where the Controller sets the Target’s Dynamic Address using a Direct CCC that references the Target’s `636` I[2] C Static Address), then that Target will never be asked to use the ENTDAA CCC. In such a case, the I3C `637` Target could participate on the I3C Bus despite not implementing ENTDAA CCC support. 

- `638` An I3C Target may choose to implement support for either or both of the SETAASA and SETDASA CCCs. 

- `639` Since both of these CCCs rely on the Controller knowing that Target’s I[2] C Static Address (and perhaps the 

- `640` Static Addresses of all other Targets as well), these methods can save time for certain use cases, although `641` they do impose some implementation requirements on the system designer. 

- `642` Nonetheless, MIPI Alliance strongly recommends supporting the ENTDAA CCC, otherwise the Device will `643` only ever be usable on that narrow subset of I3C Buses. 

## **Q16.2 How can an I3C Target lose its I3C Dynamic Address, and how does it become an I[2] C Target again?** 

- `644` Normally, once an I3C Target is assigned an I3C Dynamic Address, it will be retained until the Target is de- `645` powered. However, an I3C Target will lose its I3C Dynamic Address as a result of the RSTDAA Broadcast `646` CCC, since this resets all I3C Targets back to their initial state. After RSTDAA, I3C Targets that can also `647` operate on a Legacy I[2] C Bus (per _**Q15.2**_ ) would behave as I[2] C Targets, per the specification at `648` _**Section 5.1.2.1.1**_ . 

- `649` 

## _**Note:**_ 

- `650` _The RSTDAA Broadcast CCC is used to reset all Dynamic Addresses, typically before assigning new_ `651` _Dynamic Addresses to I3C Targets, or to return I3C Targets to their initial state._ 

- `652` 

- `653` 

An I3C Target could also lose its Dynamic Address under other circumstances, for example: 

   - The Device is reset by an out-of-band method, such as a pin-reset 

- `654` • The Device is reset by a full Target Reset (starting with I3C v1.1) which can be invoked two `655` different ways: 

- `656` • RSTACT CCC with Defining Byte 0x02, followed by Target Reset Pattern (per the specification `657` at _**Section 5.1.11.2**_ ) 

- `658` 

- `659` 

- Two consecutive Target Reset Patterns (per the specification at _**Section 5.1.11.1**_ ) 

- The Device goes into deepest-sleep (i.e., power down) 

`660` In the case of an I3C Device losing its Dynamic Address in non-standard ways, the Hot-Join mechanism `661` allows the Target to notify the Controller of the event and receive a new Dynamic Address. In cases where `662` the Controller has deliberately caused the Target to lose its Dynamic Address (e.g., by sending the RSTDAA `663` CCC, or by using a Target Reset), the I3C Controller will start a new Dynamic Address Assignment process `664` using the ENTDAA, SETDASA, or SETAASA CCCs. 

- `665` 

- `666` 

## _**Note:**_ 

   - _See also_ _**Q16.8** for CCCs that can change a currently assigned Dynamic Address._ 

- `667` _See also_ _**Q20.1** for Offline Mode for I3C Targets, where the Devices retain their Dynamic Addresses_ `668` _through a power-down or deepest-sleep cycle._ 

## **Q16.3 What is a Provisioned ID, and why is it needed?** 

`669` During Bus initialization, the I3C Controller assigns a 7-bit Dynamic Address to each Device on the I3C Bus. `670` For this to happen, each Target device must have a 48-bit Provisioned ID (that is, each Target is provisioned `671` with its ID). The Provisioned ID has multiple fields, including MIPI Manufacturer ID and a vendor-defined `672` part number. 

Copyright © 2018–2022 MIPI Alliance, Inc. 

23 

**Public Release Edition** 

FAQ for MIPI I3C v1.1.1 & MIPI I3C Basic v1.1.1 

FAQ Version 1.1 22-Aug-2022 

## `673` _**Note:**_ 

`674` _The I3C Target may also have a Static Address. If the Controller knows this Static Address, then the_ `675` _Dynamic Address can be assigned faster._ **Q16.4 How do the first 32 bits of the Provisioned ID (PID) work? Are they random or fixed?** 

`676` The first part of the PID contains a unique Manufacturer ID. Companies need not be MIPI Alliance members `677` to be assigned a unique Manufacturer ID. 

`678` The second part of the PID normally contains a part number (which is normally divided up into general and `679` specific part info for that vendor), as well as possibly an instance number which allows for multiple instances `680` of the same device on the same I3C Bus. The instance ID is usually fed from a pin-strap, fuse(s), or non- `681` volatile memory (NVM). 

`682` A random number may be used for the part number, although normally only for test mode, as set by the `683` Controller using the ENTTM (Enter Test Mode) CCC. When a Device that supports random values enters `684` the test mode, the PID[31:0] bits are randomized. When the Controller exits the test mode, the Devices reset `685` bits PID[31:0] to their default value. 

- `686` _**Note:**_ 

`687` _The use of a random number in the PID allows for many instances of the same Device to be attached_ `688` _to a gang programmer/tester, relying on the random number to uniquely give each a Dynamic_ `689` _Address. However, the random number should not be used for typical I3C applications where I3C_ `690` _Devices must be uniquely identified, especially by higher-level software that runs on the Application_ `691` _Host that is driving the I3C Controller._ 

## **Q16.5 What if the Controller detects a collision during Dynamic Address Assignment with the ENTDAA CCC?** 

`692` With most configurations this is not possible, because each Device will have its own Manufacturer ID and a `693` unique part number; as a result, no collisions are possible. But if more than one instance of the same Device `694` (product) is used on a given I3C Bus, then each such instance must have a separate instance ID; otherwise `695` there would be a collision. Likewise, if any Device is using a random number for its part number (i.e., in the `696` PID), then multiple instances from that manufacturer could collide (i.e., could have the same random value `697` that time). 

`698` If the Controller knows the number of Devices on the I3C Bus, then it can detect this condition: the number `699` of Dynamic Addresses assigned would be less than the expected number of Devices. If that is detected, then `700` the I3C Controller can take steps to resolve such collisions, for example by resetting all Dynamic Addresses `701` with the RSTDAA CCC and restarting the process, or by declaring a system error after a set maximum `702` number (e.g., 3) of such attempts fail. 

## **Q16.6 What CCCs must an I3C Target support before a Dynamic Address is assigned?** 

`703` All I3C Targets must be able to process Broadcast CCCs at any time, whether or not they have been assigned `704` a Dynamic Address. I3C v1.1.1 and I3C Basic v1.1.1 clarify the I3C Target requirements (see the `705` specifications at _**Section 5.1.2.1**_ ) and also clarify which CCCs are required to be supported (see _**Q18.7**_ and `706` the specifications at _**Section 5.1.9.3**_ ). 

`707` **Example:** An I3C Device may act as an I²C device before it receives its assigned Dynamic Address. However, `708` the Device is still expected to ACK the START with the Broadcast Address (7’h7E). The only exception `709` would be if the Device were to choose to remain an I²C-only device; in this case, the Device would leave any `710` 50 ns spike filter enabled (see the specifications at _**Section 5.1.2.1**_ ). 

- `711` _**Note:**_ 

`712` _Devices that do recognize START with the Broadcast Address could see any CCC (not just ENTDAA,_ `713` _SETDASA, or SETAASA). When determining what effect each CCC will have, these Device may take_ `714` _into account whether or not the Device has received an assigned Dynamic Address. For example, if_ `715` _the Device has not yet received its assigned Dynamic Address, then receipt of the RSTDAA CCC_ `716` _should probably have no effect._ 

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

24 

FAQ Version 1.1 22-Aug-2022 

FAQ for MIPI I3C v1.1.1 & MIPI I3C Basic v1.1.1 

## **Q16.7 What implicit state or configuration is required for an I3C Device that supports Group Addressing?** 

- `717` Typically, an I3C Device that supports Group Addressing can be assigned to one or more Group Addresses, `718` but has the same I3C Target configuration and state as any other I3C Target (i.e., its role does not change). In `719` effect, this Device gains the ability to receive I3C transfers that are addressed (i.e., targeted) to the Group `720` Addresses to which it might be currently assigned, but the same configuration or state applies to the entire `721` Target, equally for its assigned Dynamic Address as well as any and all assigned Group Addresses. 

- `722` For some configuration changes, the I3C Controller may use certain Direct CCCs to configure an I3C Target, `723` either individually (i.e., by sending the Direct Write or Direct SET CCC to its Dynamic Address) or in a `724` multicast manner (i.e., by sending the Direct SET CCC to the assigned Group Address). When used as a `725` multicast, the Direct CCC is received by all I3C Targets that are assigned to that Group, and all such I3C `726` Targets apply the same configuration change (if that CCC is supported), exactly as though each I3C Target `727` had received the same Direct CCC addressed to its Dynamic Address. No other internal state is required, and `728` no difference in behavior is expected, when such Direct CCCs are sent to a commonly-assigned Group `729` Address vs. each individual Dynamic Address (see the specification at _**Section 5.1.9.4**_ ). 

- `730` For other configuration changes, specifically for Multi-Lane configuration changes (if the I3C Target `731` supports Multi-Lane transfers and separate Group Address configurations for Multi-Lane transfers, as defined `732` in specification _**Section 5.3.1.1.1**_ ), a Direct CCC sent to a Group Address is a special configuration operation, `733` and the I3C Target must store this configuration differently than it would for the equivalent Direct CCC sent `734` to its Dynamic Address. The MLANE CCC is a special case requiring different handling, where the Group `735` Address must be treated specially (i.e., differently than the MLANE CCC sent to a Dynamic Address). 

- `736` Other Direct CCCs are defined in a different way, and the I3C Target must treat Group Addresses specially. `737` Certain Direct CCCs should never be sent to a Group Address (see the specification at _**Section 5.1.2.1.3**_ and `738` _**Section 5.1.9.4**_ .) 

- `739` _**Note:**_ 

- `740` _**Section 5.1.4.4** in v1.1 of the I3C specification has a technical inaccuracy when it states that the_ `741` _SETGRPA CCC “assigns and unassigns a Group Address” to I3C Devices. In fact, the SETGRPA_ `742` _CCC only assigns a Group Address, it does not unassign a Group Address. This misstatement has_ `743` _been corrected in v1.1.1 of the I3C specification._ 

## **Q16.8 Can any CCCs change or override an I3C Target’s assigned Dynamic Address?** 

- `744` Per _**Section 5.1.4**_ , a currently assigned Dynamic Address can only be changed if the Controller sends the `745` SETNEWDA Direct CCC (if supported) or the RSTDAA Broadcast CCC. No other CCCs will change a `746` currently assigned Dynamic Address. This applies regardless of how the Dynamic Address was originally `747` assigned (i.e., either via ENTDAA, SETDASA, or SETAASA). 

- `748` If the Target also supports the optional SETDASA or SETAASA CCCs, then these only assign the Dynamic `749` Address if it was not already assigned: 

- `750` 1. The Target will only respond to (i.e., will only ACK) and act on the SETDASA CCC sent to its `751` Static Address if the Target did not already have an assigned Dynamic Address at that time. If a `752` Dynamic Address was already assigned, then the SETDASA CCC has no effect. 

- `753` 2. The Target will only act on the SETAASA Broadcast CCC sent to the I3C Bus if it did not already `754` have an assigned Dynamic Address at that time. However, the Target must still provide ACK (as `755` with any Broadcast CCC) but the SETAASA CCC will have no effect. 

- `756` Additionally, per _**Section 5.1.9.3.4**_ , a Target that already has an assigned Dynamic Address will not respond `757` to the ENTDAA CCC. 

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

25 

FAQ for MIPI I3C v1.1.1 & MIPI I3C Basic v1.1.1 

FAQ Version 1.1 22-Aug-2022 

## **Q16.9 Are I3C Targets required to provide ACK for Broadcast CCCs that are not supported?** 

`758` Yes. If an I3C Target is powered and knows that it is on an I3C Bus, then it must provide ACK to the Broadcast `759` Address in the SDR Frame (i.e., after a START or Repeated START). This also applies to Broadcast CCCs `760` sent in SDR Mode: an I3C Target must provide ACK to the Broadcast Address before it receives the `761` Command Code for the Broadcast CCC, even if the Target does not support that particular CCC (see _**Q14.2**_ `762` _**Q16.6**_ , and _**Q17.4**_ ). 

- `763` 

## _**Note:**_ 

- `764` _This also applies to the ENTHDR0 – ENTHDR7 Broadcast CCCs that put the I3C Bus into an HDR_ `765` _Mode. If the Target does not support that particular HDR Mode, then it must still provide ACK to such_ `766` _a Broadcast CCC in the SDR Frame, then after seeing the ENTHDRx CCC that it does not support,_ `767` _it must ignore all activity on the Bus until it sees the HDR Exit Pattern (per specification_ _**Section 5.2**_ `768` _and_ _**Section 5.2.1** ). Additionally, if the Target did not support such an HDR Mode, it would be unable_ `769` _to recognize the use of the Broadcast Address in subsequent HDR commands (e.g., for CCCs sent_ `770` _in HDR Modes)._ 

- `771` _The only exception to this requirement is if this is a Hot-Joining Target that is not yet safely on the_ `772` _I3C Bus (see_ _**Q17.4** ). Such a Target must wait to either see the Bus Idle condition (i.e., for the_ `773` _standard Hot-Join method) or otherwise determine that it is on an I3C Bus by watching for special_ `774` _activity (i.e., for a passive Hot-Join method; see_ _**Q17.7** ); before this point, it would not have emitted_ `775` _its Hot-Join Request. In such a case, the Hot-Joining Target would not be able to recognize valid I3C_ `776` _Bus activity._ 

## **2.17 In-Band Interrupt and Hot-Join** 

## **Q17.1 What changed with In-Band Interrupts (IBIs) in I3C v1.1.1?** 

`777` While the definition of In-Band Interrupts has not changed in I3C v1.1.1, some of the details of the Pending `778` Read Notification contract (see specification _**Section 5.1.6.2.2**_ ) have been clarified. An I3C Target Device `779` may only queue one active Pending Read Notification (i.e., a single message that will be read with either an `780` SDR Private Read, or an HDR Generic Read) at a time; and it may now send another IBI if the I3C Controller `781` has not followed up to read the enqueued data for the Pending Read Notification: 

- `782` • This IBI may be a reminder, using the same Mandatory Data Byte value that was sent earlier (i.e., `783` it cannot be another MDB value that is also used for Pending Read Notifications). 

- `784` • If so, then it is forbidden to use it to indicate that additional Pending Read Notifications are `785` waiting (i.e., that they are active and are enqueued after this notification), and the Controller is `786` not obligated to keep count of these IBIs. 

- `787` • Alternatively, this IBI may also indicate an error code or some other condition (i.e., due to delayed `788` read). 

- `789` • However, the I3C Target must still keep the data available to read, if it can. 

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

26 

FAQ Version 1.1 22-Aug-2022 

FAQ for MIPI I3C v1.1.1 & MIPI I3C Basic v1.1.1 

```
790
791
```

```
792
```

```
793
```

```
794
```

```
795
```

```
798
```

```
799
```

```
800
```

## **Q17.2 How can an I3C Controller support Pending Read Notifications?** 

I3C Controller Devices that comply with the MIPI I3C Host Controller Interface specification (i.e., I3C HCI v1.0 _**[MIPI02]**_ or v1.1 _**[MIPI12]**_ ) can easily support Pending Read Notifications. MIPI I3C HCI already defines a standard feature known as “Auto-Command” that conforms to the Pending Read Notification contract and enables (in SDR Mode) automatic initiation of Private Reads or (in supported HDR Modes) Generic Reads in hardware, without software intervention, based on matching MDB values in IBIs received from I3C Target Devices. 

```
796
```

```
797
```

```
801
```

```
802
```

```
803
```

Implementers of other I3C Controller Devices could choose to offer support for Pending Read Notifications as a feature in hardware and/or firmware, with varying degrees of configurability. In situations where hardware or firmware support is not feasible, an I3C Controller Device and its Host could also support this in software, provided that the Host’s software upholds all the expectations in the Pending Read Notification contract (see specification _**Section 5.1.6.2.2**_ ). Note that this may require the ability to pause or cancel any previously enqueued Read transfers if the I3C Controller receives such an IBI with matching MDB value to signal a Pending Read Notification, as this would oblige the I3C Controller or its Host to initiate a Read (i.e., SDR Private Read or HDR Generic Read) that is expected for this particular IBI. 

## **Q17.3 What is Hot-Join?** 

`804` The I3C Bus protocol supports a mechanism for Targets to join the I3C Bus after the Bus is already `805` configured. This mechanism is called Hot-Join. The I3C specification defines the conditions under which a `806` Target can do this, e.g., a Target must wait for a Bus Idle condition. 

## **Q17.4 Is an I3C Target required to receive and process the Broadcast ENEC, DISEC, and other Bus-state CCCs before sending a Hot-Join Request, or before being assigned a Dynamic Address?** 

`807` Yes. An I3C Target is expected to monitor Broadcast CCCs; the special exception is for Hot-Join Targets, as `808` explained below. 

`809` Under most circumstances the Target should process all supported Broadcast CCCs, however the Target is `810` specifically required to process supported Broadcast CCCs that affect Bus state. This includes the ENTHDRn `811` CCCs (which turn the HDR Exit Detector on), as well as the ENEC and DISEC CCCs for whatever events `812` the Target supports (e.g., IBI). 

`813` _**Note:**_ 

`814` _As a practical matter, the I3C Primary Controller will not generally use any CCCs other than Dynamic_ `815` _Address assignment while bringing up the I3C Bus. However, it is allowed to use Bus state CCCs as_ `816` _needed._ 

`817` For a Hot-Join Target (i.e., a Target that needs to emit a Hot-Join Request to receive a Dynamic Address), `818` this rule only applies once the Target is safely on the I3C Bus and eligible to emit a Hot-Join Request. Such `819` a Target might also join the Bus without knowing the current state, so in order to know that a Broadcast CCC `820` is being sent it needs to see a period of inactivity followed by a valid START with the Broadcast Address. `821` I3C v1.1.1 and I3C Basic v1.1.1 clarify these rules for Hot-Join eligibility; see also _**Q17.10**_ . In such cases,a `822` Target that has not yet seen a START and has also not become eligible to emit the Hot-Join Request might `823` need to wait for a Bus Available Condition (per specification _**Section 5.1.3.2.2**_ ) before it can see a START; `824` or a Bus Idle Condition ( _**Section 5.1.3.2.3**_ ) before it would be eligible to pull SDA Low to initiate a START `825` to emit its own Hot-Join Request (i.e., using the standard method). 

`826` So, as a general rule, the Target will emit the Hot-Join Request before the I3C Controller is able to emit any `827` Broadcast CCCs. However, after that the Target may see one or more Broadcast CCCs prior to being assigned `828` a Dynamic Address. 

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

27 

FAQ for MIPI I3C v1.1.1 & MIPI I3C Basic v1.1.1 

FAQ Version 1.1 22-Aug-2022 

## **Q17.5 Is an I3C Target required to wait the full 1 ms before it can send a Hot-Join Request?** 

## `829` _**Note:**_ 

```
830
```

```
831
```

```
832
```

```
833
```

```
834
```

_This question does not apply to I3C Basic v1.0 and I3C v1.1._ 

In I3C v1.0, an I3C Target was required to wait 1 ms (i.e., the tIDLE minimum value) before it could send a Hot-Join Request. Newer versions of the I3C specification define a new tIDLE minimum value of 200 µs, since that is sufficient for all valid uses. I3C v1.0 devices may choose to support that smaller delay now. I3C Basic v1.0 and I3C v1.0 already support a tIDLE minimum value of 200 µs. 

`835` _**Note:**_ 

`836` _The new tIDLE minimum value of 200 µs is safe, as SCL at High in HDR Mode cannot exceed 100 µs_ `837` _(i.e., assuming a typical duty cycle) since the minimum I3C Bus frequency being 10 KHz._ 

## **Q17.6 Can I3C Hot-Join Target Devices be used on a Legacy I[2] C bus?** 

```
838
```

Only if they have a way to turn the Hot-Join feature off, or if passive Hot-Join is supported. (See _**Q17.7**_ ) 

`839` Hot-Join Requests are not compatible with Legacy I[2] C controllers, so Hot-Join would have to be disabled for `840` the Target to be used on a Legacy I[2] C bus. The disabling of the Hot-Join feature should be done via some `841` feature that is not part of the I3C protocol (i.e., not via the DISEC CCC), since an I[2] C controller does not `842` support the I3C protocol. 

## **Q17.7 Can an I3C Target support Hot-Join when used on an I3C Bus, and still function correctly on a Legacy I[2] C Bus?** 

`843` Yes, but only if it supports the passive Hot-Join method defined in specification _**Section 5.1.5.3**_ . If the Target `844` does not support passive Hot-Join, then see _**Q17.6**_ . 

`845` Before initiating the Hot-Join Request, a Target that supports passive Hot-Join must first ensure that it is `846` actually on an I3C Bus. This can be done by waiting for a recognizable end of an SDR Frame that ends with `847` a STOP. The key difference is that in order to determine that this is actually an I3C Bus, the Target must first `848` see an SDR Frame addressed to the Broadcast Address (7’h7E / W). Following this, the Target could either `849` pull SDA Low to drive a START condition, or wait to see a START that another I3C Device initiates, before `850` emitting the Hot-Join Request (i.e., arbitrating the special Hot-Join Address 7’h02 into the Arbitrable Address `851` Header following the START). 

`852` _**Note:**_ 

`853` _A passive Hot-Joining Target needs to see an SDR Frame that is addressed to the Broadcast Address_ `854` _in order to determine that the Bus is in SDR Mode. Without this knowledge, such a Target might see_ `855` _Bus activity in HDR Modes and misinterpret it as STARTs and STOPs. Alternatively, a passive_ `856` _Hot-Joining Target could wait for the HDR Exit Pattern because it clearly indicates a return to SDR_ `857` _Mode._ 

`858` _The detection of an SDR Frame that is addressed to the Broadcast Address is critical because a_ `859` _passive Hot-Joining Target might not engage its timer or oscillator (i.e., to check for Bus Idle or Bus_ `860` _Available condition) until it determines that it is on an I3C Bus and that the Bus is in SDR Mode._ `861` _Without this detection, such a Target will not know whether it is safe to emit the Hot-Join Request._ 

`862` If the Target ensures that it is indeed on an I3C Bus in this manner, then it must observe the standard behaviors `863` of an I3C Target that has not yet received a Dynamic Address, as defined in specification _**Section 5.1.2.1**_ `864` The Target must acknowledge the Broadcast Address (7’h7E), which means that it is required to understand `865` and process all required CCCs, including ENEC and DISEC. Such a Target is not eligible to respond to the `866` ENTDAA CCC before it has emitted the Hot-Join Request at least once. 

`867` A Target that supports both standard and passive Hot-Join methods is free to either A) Initiate a START, wait `868` for the appropriate time (i.e., Bus Idle condition), emit the Hot-Join Request, and then pull SDA Low like a `869` standard Hot-Joining Device; or B) Wait for a START that another I3C Device emits (i.e., after waiting for `870` Bus Idle condition). 

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

28 

FAQ Version 1.1 22-Aug-2022 

FAQ for MIPI I3C v1.1.1 & MIPI I3C Basic v1.1.1 

## **Q17.8 Can multiple I3C Targets use the same reserved Hot-Join Address, or can multiple Hot-Joining I3C Targets raise a Hot-Join Request at the same time?** 

`871` Yes, the reserved Hot-Join Address (7’h02) is safe even if multiple I3C Targets all simultaneously attempt to `872` emit a Hot-Join Request. If multiple I3C Targets do join the I3C Bus and all become eligible to emit the Hot- `873` Join Request (per specification _**Section 5.1.5**_ ) at the same time, then they would be expected (and allowed) `874` to all emit the Hot-Join Request at the same time. Since a Hot-Join Request is a special form of the In-Band `875` Interrupt Request with no data payload (i.e., no Mandatory Data Byte), multiple I3C Targets may all emit `876` this request at the same time, provided that they are all eligible to do so. 

`877` **Example:** As one I3C Target pulls SDA Low to initiate the START Request and drive the 7’h02 Hot-Join `878` Address into the Arbitrable Address Header, and the other eligible I3C Targets see this activity while they are `879` eligible, they would also emit the same Hot-Join Address and behave accordingly. This could be useful if one `880` such I3C Target supported the standard Hot-Join method and waited for the Bus Available condition, while `881` another such I3C Target only supported a passive Hot-Join method but was waiting for another I3C Device `882` to initiate a START Request. 

`883` Upon receiving the Hot-Join Request and responding with ACK, the Controller sends the ENTDAA CCC `884` (per specification _**Section 5.1.4.2**_ ) to signal its intent to start the Dynamic Address Assignment procedure and `885` assign Dynamic Addresses to all I3C Targets that have not yet received one. Since the Dynamic Address `886` Assignment procedure inherently supports detection of multiple I3C Targets and uses Arbitration to select `887` one I3C Target at a time (i.e., for each iteration of assignment), the Controller should continue the Dynamic `888` Address Assignment procedure so it can catch all eligible I3C Targets that emitted the Hot-Join Request `889` together (as well as any that might have previously emitted the Hot-Join Request). 

`890` See _**Q17.10**_ for more information about Hot-Join Requests and the specification clarifications that are new `891` for I3C v1.1.1. 

## **Q17.9 In a Hot-Join, when should the DISEC CCC be sent? After ACK, or after NACK?** 

`892` After the NACK is preferred, but after the ACK is also acceptable. 

`893` The Hot-Join mechanism allows the Controller to first NACK, and then send the DISEC CCC with the DISHJ `894` bit set to disable subsequent Hot-Join Requests. If the Controller ACKs the Hot-Join Request, then that is `895` interpreted as a promise that the Controller will eventually send the ENTDAA CCC to assign a Dynamic `896` Address to the Target(s) that emitted the Hot-Join Request. 

`897` If the Controller were to send a subsequent DISEC CCC with the DISHJ bit set, then that would cancel this `898` promise, but it would also leave the Target(s) with no Dynamic Address. 

- `899` _**Note:**_ 

`900` _If any additional Targets joined the Bus after the DISEC CCC was sent, then they would not have_ `901` _seen the DISEC CCC, and as a result would likely send their own Hot-Join Requests._ 

```
902
```

See _**Q17.10**_ for additional clarifications and updates in I3C v1.1.1 and I3C Basic v1.1.1. 

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

29 

FAQ for MIPI I3C v1.1.1 & MIPI I3C Basic v1.1.1 

FAQ Version 1.1 22-Aug-2022 

## **Q17.10 What has changed regarding Hot-Join in I3C v1.1.1?** 

`903` In the I3C v1.0, I3C Basic v1.0, and I3C v1.1 specifications, the requirements for Hot-Join were not clearly `904` defined and the _**Annex C**_ Hot-Join FSM diagram did not illustrate all of the possible intended flows. 

`905` The I3C WG received implementer feedback on these points, and in I3C v1.1.1 clarified the normative `906` requirements for a Hot-Joining Device. The WG also added a new definition of the Hot-Join procedure which `907` is now defined separately from the Target requirements. In addition, the _**Annex C**_ Hot-Join FSM diagram `908` now informatively illustrates a typical flow, rather than being presented as a representation of all possible `909` Hot-Join Request flows. 

`910` To summarize the Hot-Join changes: 

- `911` • A Hot-Joining Device that has not yet raised the Hot-Join Request (i.e., an In-Band Interrupt to the `912` Reserved I3C Address of 7’h02 with Write) does not follow the standard behaviors of an I3C `913` Target that has not yet received a Dynamic Address (as defined in specification _**Section 5.1.2.1**_ ), `914` with the following exceptions: 

- `915` • If the Target supports a passive Hot-Join method (specification _**Section 5.1.5.3**_ ) and will be `916` using that method instead of the standard Hot-Join Request (which usually requires the I3C Bus `917` to go idle long enough to satisfy the Bus Idle Condition), then it must verify that the bus it is on `918` is on an I3C Bus by watching for an SDR Frame. _**Q17.7**_ provides more clarity on the `919` requirements for Targets that support passive Hot-Join. 

- `920` • The Controller may choose to either ACK or NACK the Hot-Join Request, and may then send the `921` ENTDAA CCC afterwards: 

- `922` • This may happen either immediately (i.e., after the next Repeated START), or later (i.e., after a `923` prolonged period). The ENTDAA CCC might not be in the same SDR Frame, since the `924` Controller may choose to send this after a STOP, followed by a delay (i.e., Bus Free Condition `925` or longer) and then a START. Optionally, the Controller may initiate other transfers and/or `926` CCCs between the ACK/NACK and the ENTDAA CCC. 

- `927` • In short, any valid actions are allowed between the ACK/NACK and ENTDAA CCC, and the `928` Target should still respond to the ENTDAA CCC appropriately. If the Target knows that it needs `929` a Dynamic Address and it has already raised the Hot-Join Request, then it should be ready to `930` respond to the ENTDAA CCC when the Controller starts the Dynamic Address Assignment `931` procedure. 

- `932` • If the Controller provided an ACK to the Hot-Join Request, then any Targets that raised the `933` Hot-Join Request must remember that an ACK was provided, cease raising Hot-Join Requests, `934` and remain ready to participate in a subsequent ENTDAA CCC (which the Controller should `935` send at a later time). The Target should not send a subsequent Hot-Join Request if the Controller `936` is slow to start the ENTDAA procedure. 

- `937` • Although providing an ACK for a Hot-Join Request is a typical flow, providing a NACK is also `938` acceptable. The Target should remain ready to respond to the ENTDAA CCC in either case, `939` even if the Target receives a NACK or is told by the Controller to stop sending Hot-Join `940` Requests (i.e., using the DISEC CCC with the DISHJ bit set). 

- `941` • Note that the Controller may choose to send the DISEC CCC with the DISHJ bit set, after either `942` providing an ACK or a NACK to a Hot-Join Request (see _**Q17.9**_ ). 

- `943` • Any Targets that have already raised a Hot-Join Request are required to also respond to other `944` required CCCs, per specification _**Section 5.1.2.1**_ which defines the standard behaviors for an I3C `945` Target that has not yet received a Dynamic Address: 

- `946` • Such Targets must acknowledge the Broadcast Address (7’h7E). This means they are required to `947` understand and process all required CCCs, including ENEC and DISEC. (Targets that support `948` passive Hot-Join methods are already required to do this, once they successfully determine that `949` they are indeed on an I3C Bus; see _**Q17.7**_ ). 

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

30 

FAQ Version 1.1 22-Aug-2022 

FAQ for MIPI I3C v1.1.1 & MIPI I3C Basic v1.1.1 

- `950` • After either providing ACK or NACK in response to the Hot-Join Request, the Controller may `951` send (and such Targets are required to properly receive) the DISEC CCC with the DISHJ bit set. `952` The Controller doing so is required to prevent any Targets that raised a Hot-Join Request and `953` received a NACK from subsequently attempting to raise a Hot-Join Request. 

- `954` • Subsequently, the Controller may send (and such Targets are required to properly receive) the `955` ENEC CCC with the ENHJ bit set, to effectively re-enable Hot-Join Requests on the I3C Bus. `956` Any eligible Targets that receive this ENEC CCC and that previously received the DISEC CCC `957` with the DISHJ bit set may choose to re-send the Hot-Join Request if these Targets both (1) are `958` capable of doing so, and (2) had originally emitted a Hot-Join Request, and (3) have not yet `959` received a Dynamic Address. 

- `960` • If the Active Controller is a Secondary Controller Device that is not capable of processing `961` Hot-Join or Dynamic Address Assignment, or one that wishes to defer processing to a more `962` capable Controller (i.e., to the Primary Controller), then it may choose to disable Hot-Join on `963` the I3C Bus by sending the DISEC CCC with the DISHJ bit set. It may then pass the Controller `964` Role to any other Controller-capable Device, including but not limited to the Primary Controller. 

## **2.18 Common Command Codes (CCCs)** 

## **Q18.1 What are the differences between I3C v1.0 and I3C v1.1 in how CCCs are defined?** 

- `965` CCCs in I3C v1.1 are defined and marked differently than in I3C v1.0, in two important ways: 

- `966` 1. **Conditionally Required CCCs:** In the I3C v1.1 specification, _**Table 16**_ in _**Section 5.1.9.3**_ (i.e., the `967` main table that defines the I3C Common Command Codes) now marks every CCC as either `968` Required (‘R’), Conditional (‘C’), or Optional (‘O’). Required and Optional retain the same `969` meanings they had in I3C v1.0, but in I3C v1.1 some CCCs have been changed to Conditional. `970` For Conditional CCCs the Description column includes a note indicating the condition(s) under `971` which the CCC is required (“Required If:”). Typical conditions would be the use of a particular `972` feature, or support for another particular CCC. If the conditions for a given Conditional CCC are `973` not met, then there is no requirement to support that CCC, and support for it can be regarded as `974` Optional. 

- `975` **Example:** The ENTAS0 CCC is marked as Conditional and only “Required If” any of the other `976` ENTASx CCCs (i.e., ENTAS1, ENTAS2, and/or ENTAS3, all of which are Optional) are `977` supported. Of course, an implementer may choose to support the ENTAS0 CCC even if none of `978` these other Optional ENTASx CCCs are supported. But if at least one of the other ENTASx CCCs `979` are supported, then support for the ENTAS0 CCC is required for that configuration. 

- `980` 2. **CCCs in HDR Modes:** At the discretion of the implementer, CCCs may also be supported in any `981` supported HDR Modes. Specification _**Section 5.2.1.2**_ defines the general concepts of CCC `982` framing while in HDR Modes, and specifies key requirements and details regarding their use `983` within an HDR Mode. In general, the use of CCCs within any HDR Mode provides the option to `984` send certain CCCs efficiently while remaining in HDR Mode (i.e., without the extra overhead of `985` exiting HDR Mode and then returning to SDR Mode). The specific CCC framing details for each `986` supported HDR Mode are listed in _**Table 53**_ and defined in the sections specifying each HDR `987` Mode. 

- `988` _**Table 51**_ defines which CCCs may be supported and permitted for use in any HDR Mode, both for `989` Broadcast CCC and Direct CCC flows. Additionally, _**Table 52**_ defines which CCCs are prohibited `990` in any HDR Mode and explains why. Since support for CCCs in HDR Modes is optional, and `991` since an implementer might choose to support a subset of CCCs from _**Table 16**_ (i.e., those which `992` are also permitted for use, as per _**Table 51**_ and _**Table 52**_ ), it is important for the I3C Controller to `993` know which CCCs are supported in HDR Modes. This might include CCCs set aside for Vendor / `994` Standard Extension use, or ones reserved for another MIPI Alliance WG. It is also required that `995` any CCC that is supported in any HDR Mode is supported in SDR Mode too. 

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

31 

FAQ for MIPI I3C v1.1.1 & MIPI I3C Basic v1.1.1 

FAQ Version 1.1 22-Aug-2022 

`996` _**Note:**_ 

`997` _This last point means that if an I3C Device does not acknowledge a given CCC in a given HDR_ `998` _Mode, then the I3C Controller can determine whether that CCC is only unsupported in that HDR_ `999` _Mode (vs. is not supported at all) by retrying that same CCC in SDR Mode._ 

## **Q18.2 Does the mandated "single-retry model" apply to all Directed Read CCCs?** 

- `1000` At _**Section 5.1.9.2.3**_ the I3C v1.1 specification states: “I3C mandates a single-retry model for Direct GET `1001` CCC Commands.” Based on this statement, adopters have a general notion that the Controller is required to `1002` retry once for the Directed GET CCCs if the Target NACKs the first try. This may not be applicable for other `1003` “read” Directed CCCs (such as RSTACT, MLANE, vendor read, etc.) that are not defined for dedicated Read `1004` CCCs (i.e., CCCs that have names of the form GETxxx). 

## **Q18.3 What has changed in CCC use or coding in I3C v1.1 or v1.1.1?** 

- `1005` The coding and framing details for CCCs have been changed or extended, in three important areas: 

- `1006` 1. **Direct Write/Read Commands:** In I3C v1.0, Direct CCCs were either Direct Read Commands `1007` (Direct GET CCC) or Direct Write Commands (Direct SET CCC). I3C v1.1 adds an additional `1008` Direct Write/Read Command (Direct SET/GET CCC) form: a Direct Write immediately followed `1009` by a Direct Read with the same Command Code. This form is used for alternately writing to, and `1010` then reading data from, one or more specific I3C Target Devices. The Direct Write/Read `1011` Command uses the Direct CCC framing model per specification _**Section 5.1.9.2.2**_ . 

`1012` **Example:** An I3C Controller might use the MLANE CCC ( _**Section 5.1.9.3.30**_ ) to configure an I3C `1013` Target Device to use a specific Multi-Lane configuration using a Direct SET CCC, followed by a `1014` Direct GET CCC to read back the active Multi-Lane configuration and confirm that it was selected `1015` for operation. Using both forms of Direct SET CCC and Direct GET CCC within the same SDR `1016` frame is considered a Direct SET/GET CCC. 

- `1017` 2. **Defining Byte for Directed CCCs:** In I3C v1.1, some Directed CCCs add support for a Defining `1018` Byte: 

- `1019` A. In CCC framing for SDR Mode, the coding of the initial CCC is: 

   - S, 7’h7E, CCC_byte, Defining_Byte, Sr, Target_Addr, .... 

- `1020` For more framing details for SDR Mode, see _**Table 15**_ in _**Section 5.1.9.1**_ . 

- `1021` B. In CCC framing for HDR Modes, the Defining Byte is sent in the HDR-x CCC Header Block `1022` of type Indicator. This framing element is defined differently for each HDR Mode; for more `1023` framing details, see _**Table 53**_ in _**Section 5.2.1.2.1**_ . 

`1024` Depending on the particular CCC, this Defining Byte can be used in several possible ways: 

- `1025` • It might define a register/code to set, either with or without additional per-Target info 

- `1026` 

   - It might select a particular register/code to read, from among several available for that CCC 

- `1027` • It might indicate one of several completely different sub-commands, each of which might be `1028` either required or optional, as needed for the particular CCC definition and use case. 

- `1029` **Example:** When used with the MLANE CCC, a Defining Byte selects a sub-command. One sub- `1030` command might be used to read the available Multi-Lane capabilities for an I3C Target Device, as `1031` a Direct GET CCC; another sub-command might be used to either configure an I3C Target Device `1032` to use a specific Multi-Lane configuration, or read back the same active Multi-Lane configuration, `1033` as either a Direct GET CCC or a Direct SET CCC. For this use case, each Defining Byte has a `1034` different purpose and a different, specific data format. 

- `1035` **Example:** A Defining Byte for the GETCAPS CCC (see _**Section 5.1.9.3.19**_ ) selects among several `1036` different capabilities areas, to read from an I3C Target Device as a Direct GET CCC. For this use `1037` case, the Defining Byte may also indicate different formats for the data message returned by the `1038` I3C Target Device. 

- `1039` For some new Direct CCCs defined in I3C v1.1, a Defining Byte is required. 

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

32 

FAQ Version 1.1 22-Aug-2022 

FAQ for MIPI I3C v1.1.1 & MIPI I3C Basic v1.1.1 

- `1040` 3. **New Optional Defining Bytes:** In I3C v1.1, some CCCs that in I3C v1.0 had no Defining Byte `1041` now do have optional Defining Bytes to extend their functionality and support other new `1042` behaviors. If the I3C Controller sends the CCC _without_ the Defining Byte then the original `1043` functionality or behavior occurs, but if the CCC is sent _with_ the Defining Byte then the optional `1044` extended functionality or new behavior is accessed (see _**Section 5.1.9.2.2**_ ). 

- `1045` Many Direct GET CCCs that allow optional Defining Bytes also have a method for indicating `1046` whether any additional Defining Bytes are supported. This support would be indicated in the data `1047` message returned by the Direct version of a particular CCC (which might be the same CCC) when `1048` sent without a Defining Byte. This allows an I3C Controller to query an I3C Target Device to `1049` determine whether this capability is supported. The particular CCCs that allow optional Defining `1050` Bytes are defined in version 1.1 of the I3C specification at _**Section 5.1.9.3**_ . Additionally, for I3C `1051` Target Devices that support such Direct CCCs and also support any optional Defining Bytes, a `1052` Defining Byte value of 0x00 generally results in the same behavior as when no Defining Byte is `1053` sent. 

- `1054` _**Note:**_ 

- `1055` _While Defining Byte support for such Direct GET CCCs is generally optional, certain Defining_ `1056` _Byte values are required or strongly recommended for certain use cases, or when used in_ `1057` _conjunction with other features or capabilities. Such Direct CCCs list these conditions or_ `1058` _recommendations, in addition to any changes in the format of the data message that might be_ `1059` _returned when a Defining Byte is used._ 

- `1060` **Example:** In I3C v1.1, an I3C Controller can use the GETSTATUS CCC (see _**Section 5.1.9.3.15**_ ) `1061` to determine the operational status of an I3C Target Device. All I3C Targets support the use of `1062` GETSTATUS without a Defining Byte. But if an I3C Target also supports the GETSTATUS CCC `1063` with any optional Defining Bytes, then the I3C Controller may also do either of the following `1064` things: 

- `1065` • Send the Direct GET GETSTATUS CCC with a Defining Byte of 0x00, to return the same data `1066` message as if no Defining Byte were used; 

- `1067` • Send the Direct GET GETSTATUS CCC with any other Defining Byte value listed in _**Table 24**_ . `1068` Any I3C Target that supports that particular Defining Byte is required to ACK the CCC and `1069` return an appropriate data message for that Defining Byte (i.e., not the standard Target Status). `1070` For example, if a Defining Byte value of 0x91 (“PRECR”) is supported, then using this `1071` Defining Byte would request the Target to return alternate status information related to the `1072` Target’s Secondary Controller capabilities. 

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

33 

FAQ for MIPI I3C v1.1.1 & MIPI I3C Basic v1.1.1 

FAQ Version 1.1 22-Aug-2022 

## **Q18.4 What are Vendor / Standard Extension CCCs, who can use them, and how are they differentiated among different uses?** 

`1073` In general, the ranges of command codes byte values that are defined for Vendor or Standards use in `1074` specification _**Table 16**_ in _**Section 5.1.9.3**_ (i.e., the main table that defines the I3C Common Command Codes) `1075` can be used by any implementer or any standards developing organization to define custom CCCs that extend `1076` I3C to accommodate new use cases. However, the definition of custom CCCs should be considered carefully `1077` because the practical issues of implementation might lead to situations where interoperability could be `1078` affected across multiple I3C Target Devices that interpret the same command code differently. 

`1079` For example, different implementers or standards groups might define a custom CCC using the same `1080` command code value (i.e., CCC byte value) with (for a Direct GET CCC) different interpretations of the `1081` message format that their custom Target Device should return, or (for a Direct SET CCC) different `1082` expectations about how their custom Target Device should act; or different expectations about which `1083` Defining Bytes might be supported for this CCC, for their custom Target Device. For these conflicting `1084` definitions, interoperability issues would certainly arise if the Controller used this custom CCC on an I3C `1085` Bus that used custom Target Devices from multiple implementers, or custom Target Devices that conformed `1086` to different standards published by several such standards groups. The Controller would not necessarily have `1087` knowledge of this situation until it detected protocol issues or encountered other errors. 

`1088` To help alleviate this situation, I3C v1.1 and I3C Basic v1.1.1 add a new SETBUSCON CCC (see `1089` specification _**Section 5.1.9.3.31**_ ) that allows the Controller to set the Bus context. This CCC informs Targets `1090` about which version of I3C is used on the Bus, and whether it is a standards-based Bus and/or a vendor- `1091` private Bus. This information allows the Target to coordinate its interpretation of extended CCCs, as well as `1092` other uses of the Bus, to match the actual current Bus context. Although the SETBUSCON feature is fully `1093` optional, it provides a powerful way to align standards-group-based uses of I3C with coordinated private `1094` uses. To foster proper coordination, SETBUSCON Context Byte values are published on the MIPI Alliance `1095` public website _**[MIPI10]**_ , and may be assigned by request. 

`1096` MIPI Alliance strongly recommends that standards groups utilize the SETBUSCON CCC to prevent such `1097` interoperability issues, by requesting an assigned Context Byte for their particular usage, which might include `1098` a specific interpretation of any command codes that are defined for vendor or Standards use. Additionally, `1099` such custom Target Device implementations should not enable this custom interpretation by default, until `1100` they receive the SETBUSCON CCC with an assigned Context Byte from the I3C Controller. 

`1101` MIPI Alliance offers a similar recommendation to implementers seeking to define custom CCCs for private `1102` use in a custom Target Device, by using similar logic in such a Target implementation to not enable this `1103` custom interpretation by default, until receiving the SETBUSCON CCC with a suitable Context Byte from `1104` the I3C Controller to explicitly enable a private interpretation. 

## **Q18.5 How should custom CCCs be used as part of a content protocol based on I3C?** 

`1105` For most use cases, custom CCCs (including the command codes that are defined for vendor or Standards `1106` use, see _**Q18.4**_ ) should generally be used as configuration or control commands, sent from an I3C Controller `1107` to one or more I3C Target Devices. Using custom CCCs for larger data transfers is not recommended. 

`1108` When considering the practical concerns of implementing support for custom CCCs in an I3C Target, it is `1109` important to note that CCCs in I3C are generally used as shorter messages that are separated from the standard `1110` content protocol (i.e., Write and Read transfers in SDR Mode, or any HDR Modes) and are not intended to `1111` interfere with normal messages sent to a Target (see _**Q12.3**_ ). 

`1112` Additionally, since the Command Code and Defining Byte for CCCs are sent to the I3C Broadcast Address `1113` 7’h7E and rely on a special ‘modality’ that must be observed by all Targets, handling for custom CCCs might `1114` need to be implemented differently within the Target. 

`1115` With these considerations in mind, implementers should consider using custom CCCs for special purposes, `1116` taking advantage of the CCC flows and their separation from the content protocol, to affect changes to the `1117` flow or meaning of transfers that are used in their content protocol. By contrast, transfers within their content `1118` protocol (such as Write or Read transfers in SDR Mode, or any HDR Modes) should be used for 

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

34 

FAQ Version 1.1 22-Aug-2022 

FAQ for MIPI I3C v1.1.1 & MIPI I3C Basic v1.1.1 

- `1119` data-intensive transactions. In most cases, custom CCCs should enable new mechanisms for configuring or `1120` controlling a Target Device, while transfers in their content protocol should be used for data transfers between `1121` a Controller and a Target. 

`1122` The following examples are provided as guidance for custom CCC definitions: 

- `1123` • Configuration commands that switch between various supported formats of index or selection that `1124` might be used in a Write command, or the first phase of a two-phase Write+Read command. `1125` • Configuration commands that send a directed mode change to particular Targets, or broadcast `1126` mode changes to all Targets that support a particular capability or feature (if applicable). `1127` • Note that custom Broadcast CCCs (i.e., for vendor or Standards use) should be used with `1128` caution, as these are received by all Targets on the I3C Bus and various Targets might handle `1129` such CCCs differently (i.e., by not using a common interpretation; see _**Q18.4**_ for guidance). `1130` • Control commands that switch between multiple endpoints within a Target, using a multiplex `1131` model that chooses how and where a standard Write transfer might be directed and processed, or `1132` where a Target might source the data message for a Read transfer. `1133` • In this case, the custom CCC acts as a command to the multiplexor logic. `1134` • However, such a multiplex model means that only one endpoint at a time can be selected for `1135` active use, and this might present a limitation for the use case, and might restrict the modality `1136` for using such a Target. `1137` • Special messages sent only to the Target hardware (i.e., the Peripheral logic) whereas the `1138` data-intensive transfers in the standard content protocol might be implemented via software or `1139` other agents that connect to the Peripheral logic, and would not need to see such special messages. `1140` • In this case, the Peripheral logic would be expected to offer a quick response due to CCC `1141` framing, so a shorter CCC message would offer rapid response due to the expectations based on `1142` capabilities in Peripheral logic, versus waiting for software or other agents to respond, which `1143` might lead to delays. `1144` • By contrast, an implementation that used Peripheral logic with software to respond to Direct `1145` GET CCCs might not be capable of successfully responding to the first such attempt, and would `1146` rely on ideal timing conditions to successfully respond to subsequent attempts. `1147` • Note that this might only apply to implementations that rely on software, versus `1148` implementations that handle custom CCCs natively (i.e., entirely within hardware). `1149` • Commands that change modes to initialize new functions or enable a new modality, which might `1150` change the interpretation of standard transfers for the content protocol (e.g., firmware download, `1151` key exchange). `1152` • For example, a custom CCC might act as a method for entering or exiting the modality in which `1153` the standard transfers are applied to a new purpose (such as transferring new firmware contents `1154` or key data). Upon exiting the modality, the new function of the Target would be applied based `1155` on the data transferred during the modality, and the standard content protocol would be used for `1156` subsequent operations with the new function. 

`1157` For other use cases that do not generally follow these guidelines, or that rely on larger message lengths for `1158` data-intensive transactions, a content protocol that primarily uses standard transfer commands (i.e., not `1159` CCCs) is strongly recommended. Using custom CCCs for data-intensive transactions on the I3C Bus might `1160` cause implementation issues for various Target Devices that are based on Peripheral logic and use “software” `1161` to handle the response for custom Direct GET CCCs. Additionally, using custom CCCs might introduce `1162` integration issues or other platform power concerns that might only appear on I3C Buses with other Target `1163` Devices which would not have been fully optimized to ignore such custom CCCs, or with other Target `1164` Devices that relied on different interpretations of custom CCCs and might not understand a particular use of `1165` SETBUSCON for the use case (as defined in _**Q18.4**_ ). For such situations, it might not be possible to predict `1166` these issues in advance until full system integration testing is performed. 

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

35 

FAQ for MIPI I3C v1.1.1 & MIPI I3C Basic v1.1.1 

FAQ Version 1.1 22-Aug-2022 

`1167` _**Note:**_ 

`1168` _Higher-level use cases could use a mix of Write/Read transfers for the content protocol, together with_ `1169` _custom CCCs for targeted configuration and control functions. Such a protocol would take advantage_ `1170` _of the strengths of CCCs, as well as the ways in which CCCs are well-suited for effective changes to_ `1171` _control, modes, or operational parameters of an I3C Target Device. For some specific aspects custom_ `1172` _CCCs might be recommended, whereas other use cases involving multiple simultaneous endpoints_ `1173` _might be better served with Virtual Target capabilities (see_ _**Q20.2** )._ 

`1174` Implementers seeking more specific guidance or recommendations should contact the I3C WG within MIPI `1175` Alliance for assistance. 

## **Q18.6 What is the new Command Code value 0x1F for CCCs, and how should it be used?** 

`1176` In I3C v1.1.1 and I3C Basic v1.1.1, a new dummy command code value 0x1F is defined for special use only `1177` in CCC flows for HDR Modes that require special structured protocol elements (i.e., Words or Blocks) to `1178` conform to that HDR Mode’s coding. This 0x1F dummy command code has no meaning as a standard CCC. `1179` But in such special flows, it takes the place of a valid CCC and is used in a valid End-of-CCC Procedure to `1180` signal the end of CCC modality and return to that HDR Mode’s standard generic HDR Write and Read `1181` transfers. Dummy command code 0x1F is currently used solely in HDR-DDR Mode, where every HDR-DDR `1182` Write must include at least one HDR-DDR Data Word. 

`1183` _**Note:**_ 

`1184` _In I3C v1.1, the equivalent End-of-CCC Procedure was incorrectly defined. Errata 01 for I3C v1.1_ `1185` _addresses this with an updated definition using this dummy command code. Implementers should_ `1186` _use only the updated definition in Errata 01 (or newer), or in I3C v1.1.1 (or newer). See_ _**Q4.4** ._ 

`1187` Dummy command code 0x1F may not be used in SDR Mode, nor in any HDR Modes other than HDR-DDR `1188` Mode. Dummy command code 0x1F has no meaning as a standard CCC. 

## **Q18.7 Which Dynamic Address Assignment CCCs is a Device required to support?** 

`1189` In I3C v1.0 and I3C Basic v1.0, support for certain CCCs relating to Dynamic Address Assignment (DAA) `1190` was defined as always required. The SETDASA CCC was originally intended to be a quicker method of `1191` assigning the initial Dynamic Address (i.e., from a fixed Static Address). In I3C Basic v1.0, the SETAASA `1192` CCC was also added in response to a request to more quickly assign all Dynamic Addresses from such fixed `1193` Static Addresses for I3C Target Devices that support these CCCs and that also have fixed Static Addresses. `1194` In both cases, support for the ENTDAA and SETNEWDA CCCs was defined as always required, as the `1195` SETDASA CCC was intended as a time-saving alternative for I3C Target Devices that also supported the `1196` ENTDAA CCC. 

```
1197
```

```
1198
```

```
1199
```

```
1200
```

```
1201
```

```
1202
```

```
1203
```

```
1204
```

```
1205
1206
```

```
1207
```

```
1208
1209
```

In I3C v1.1, the normative text for Dynamic Address Assignment in specification _**Section 5.1.4.2**_ was revised to allow the Controller to end the assignment procedure early without using the ENTDAA CCC, when it knew that all such I3C Targets already had Dynamic Addresses assigned from Static Addresses (i.e., via the SETDASA and/or SETAASA CCCs). Additionally, the SETDASA and SETAASA CCCs were defined as fully-supported options, whereas the ENTDAA CCC was defined as required except under special conditions (i.e., if a fixed Static Address was used). The SETNEWDA CCC was changed to ‘conditionally required’ status. Unfortunately, the I3C v1.1 specification text incompletely defined when this CCC should be supported, and continued to rely on assumptions about the use of this CCC (in particular, assumptions about the Controller’s ability to change a Target’s Dynamic Address) which conflicted with the CCC’s new definition as being conditionally required depending upon the use case. 

The I3C v1.1.1 specification resolves these conflicts and inconsistencies. The definition of the SETNEWDA CCC has been revised to clarify how it affects an I3C Target Device’s assigned Dynamic Address, and when the CCC may be used. 

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

36 

FAQ Version 1.1 22-Aug-2022 

FAQ for MIPI I3C v1.1.1 & MIPI I3C Basic v1.1.1 

## **Q18.8 Why was the RSTDAA Directed CCC deprecated, and why is it being removed?** 

`1210` The RSTDAA CCC originally (i.e., In I3C v1.0 and I3C Basic v1.0) had a Direct CCC form which could be `1211` used to reset a Dynamic Address for a single I3C Target. The Direct CCC form of RSTDAA was deprecated `1212` In I3C v1.1 and I3C Basic v1.1.1 because it was realized that the RSTDAA CCC should not be directed to `1213` just one Target. 

- `1214` _**Note:**_ 

`1215` _A Controller that needs to reassign one Target’s address can use the SETNEWDA CCC, if the Target_ `1216` _supports that CCC._ 

## **Q18.9 How is the GETMXDS CCC (maximum data speed) updated in I3C v1.1?** 

`1217` The standard GETMXDS CCC itself was not changed in I3C v1.1, though the definition of tSCO was clarified. `1218` However, the GETMXDS CCC now supports a Defining Byte value that allows the return of other forms of `1219` information. With no Defining Byte (or with a Defining Byte with value 0), the GETMXDS CCC behaves `1220` exactly the same as the original I3C v1.0 GETMXDS CCC. 

## **Q18.10 For Secondary Controller Devices, which format of the GETMXDS Direct CCC is used with the MSTHDLY Defining Byte?** 

`1221` In I3C v1.1, specification _**Section 5.1.7.3**_ erroneously stated that this is the GETMXDS Format 2 CCC. In `1222` fact, it is Format 3, as stated in other sections. I3C v1.1.1 corrects this error and renames the Defining Byte `1223` to CRHDLY (i.e., Controller Role Handoff Delay). 

## **Q18.11 What is the new GETACCCR CCC, and how is it different from the GETACCMST CCC?** 

`1224` In I3C v1.1.1 and I3C Basic v1.1.1, the GETACCMST CCC has been renamed to GETACCCR (Get Accept `1225` Controller Role) because the term ‘Master’ has been deprecated per _**Q5.1**_ . Note that this is only a naming `1226` change; there is no technical change. In all other respects, GETACCCR is identical to the former `1227` GETACCMST, and is used in exactly the same manner. 

## **Q18.12 What is the new DEFTGTS CCC, and how is it different from the DEFSLVS CCC?** 

`1228` In I3C v1.1.1 and I3C Basic v1.1.1, the DEFSLVS CCC has been renamed to DEFTGTS (Define list of `1229` Targets) because the term ‘Slave’ has been deprecated per _**Q5.2**_ . Note that this is only a naming change; there `1230` is no technical change. In all other respects, DEFTGTS is identical to the former DEFSLVS, and is used in `1231` exactly the same manner. 

## **Q18.13 Why has the figure for the GETCAPS CCC changed?** 

`1232` The I3C v1.1.1 specification has updated the format of the GETCAP Format 1 (Direct) CCC figure in `1233` _**Section 5.1.9.3.19**_ to make it clearer that I3C Devices that comply with I3C version 1.1 or greater are required `1234` to return at least 2 bytes for this CCC. In earlier I3C specification versions, this figure showed four possible `1235` options, one of which allowed a single data byte (i.e., GETCAP1 alone). While this was valid for an I3C `1236` Device that complied with version 1.0 and supported the GETHDRCAP CCC (the precursor to the GETCAPS `1237` CCC), it was not helpful for new I3C Device implementers. The updated figure in v1.1.1 now shows the `1238` supported options for I3C v1.1 and higher Devices. 

## **Q18.14 Why have some of the Defining Byte names changed for the GETCAPS, GETSTATUS, and GETMXDS CCCs?** 

`1239` Starting with I3C and I3C Basic v1.1.1, a number of terms used in earlier versions, including the names of `1240` some Defining Bytes, have been deprecated as detailed in _**Q5.1**_ and _**Q5.2**_ . Note that these are only naming `1241` changes; there are no technical changes. In all other respects, these Defining Bytes are identical to the ones `1242` in earlier I3C specification versions, and are used in exactly the same manner. 

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

37 

FAQ for MIPI I3C v1.1.1 & MIPI I3C Basic v1.1.1 

FAQ Version 1.1 22-Aug-2022 

## **Q18.15 Where is the Defining Byte for the SETXTIME CCC?** 

`1243` In I3C v1.1 and v1.0, the SETXTIME Broadcast and Direct CCC had a Defining Byte. However, the new `1244` Direct CCC framing model introduced in I3C v1.1 used Defining Bytes differently after the Direct CCC. `1245` This was done to allow the I3C Controller to send the Defining Byte after the Command Code and before the `1246` first Repeated START; doing so gives an individual I3C Target the opportunity to ACK or NACK its Dynamic `1247` Address, based on its cached values of the Command Code and Defining Byte (see _**Q18.3**_ ). The SETXTIME `1248` CCC’s definition of a Defining Byte was not aligned with this new standard framing model, which was a `1249` source of confusion. 

- `1250` Since the SETXTIME CCC used this byte as a Sub-Command, the I3C v1.1.1 specification now clarifies this `1251` by renaming the SETXTIME CCC Defining Byte: it is now called the Sub-Command Byte, since in the `1252` Direct CCC format the byte is sent after the Dynamic Address. 

## **Q18.16 What has changed with the ENDXFER CCC for HDR-TSP and HDR-TSL Modes?** 

- `1253` _**Note:I**_ 

- `1254` _This question does not apply to I3C Basic._ 

`1255` In I3C v1.1.1, Defining Byte values 0x7F and 0x55 now describe the process of configuring and enabling `1256` Data Transfer Early Termination in addition to the previously described HDR Ternary Flow Control. In the `1257` I3C v1.1 specification this was defined as ACK/NACK only for WRITE Commands, whereas it actually `1258` applies to all HDR-Ternary Commands. The new definition of HDR Ternary Flow Control clarifies the full `1259` set of features that these Defining Bytes (as Sub-Commands) configure. 

`1260` Additionally, specification _**Section 5.2.3.3**_ now provides more context for these capabilities, provides a better `1261` explanation of the default state of HDR Ternary Flow Control, and defines which of the procedures defined `1262` in its sub-sections apply when HDR Ternary Flow Control is enabled vs. is disabled. 

## **Q18.17 What has changed with the MLANE CCC and Multi-Lane Device configuration?** 

`1263` In I3C v1.1.1 the definition of the MLANE CCC in specification _**Section 5.1.9.3.30**_ and details of Multi- `1264` Lane Device configuration in _**Section 5.3.1.1**_ have been revised and re-written to improve clarity and resolve `1265` inconsistencies: 

- `1266` • The MLANE CCC definition was unclear about how Group Addresses can be used with the `1267` CCC’s Direct SET form. It was also unclear whether all such ML-capable I3C Devices are `1268` required to support separate ML configurations for each assigned Group Address. This has now `1269` been clarified, and the full behavior of the MLANE CCC is now described in detail. 

- `1270` • Multi-Lane configuration of I3C Devices that support multiple Addresses concurrently (i.e., Group `1271` Addresses and/or multiple Dynamic Addresses as Virtual Targets) has been clarified and expanded `1272` to cover possible cases of feature intersection. I3C v1.1.1 now describes how I3C Devices handle `1273` complex configurations, including the default configuration of newly-assigned Group Addresses `1274` based on the I3C Mode and the chosen Data Transfer Coding for Multi-Lane. 

- `1275` • Figures in _**Section 5.3**_ showing sample ML Frame formats in HDR Modes included a spurious `1276` Repeated START, after the Enter HDR CCC and before Multi-Lane transfers begin in the HDR `1277` Mode. The v1.1.1 specification corrects these diagrams; they now conform to the _**Section 5.2.1.3**_ `1278` text. 

- `1279` • In addition, the I3C WG discovered complexities regarding I3C Devices that support HDR-BT `1280` Mode and its Alternate Mode Data Transfer Codings (see specification _**Section 5.3.2.4.1**_ ) with `1281` multiple Addresses. These nuanced issues were discovered after I3C v1.1’s release and `1282` publication, and their full impact was only realized after deep review and investigation by `1283` implementers. 

- `1284` • In the v1.1.1 specification, the definitions of HDR-BT ML Data Transfer Codings address `1285` additional inconsistencies and typographical errors. 

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

38 

FAQ Version 1.1 22-Aug-2022 

FAQ for MIPI I3C v1.1.1 & MIPI I3C Basic v1.1.1 

`1286` All of these I3C v1.1.1 changes are intended to clarify Multi-Lane, in order to help resolve potential `1287` implementation issues and interoperability concerns that might have resulted in differing or incorrect `1288` interpretations, including potential assumptions that there are unstated (i.e., implicitly defined) requirements. 

## **Q18.18 How should implementers determine the minimum values for Set Max Write Length (SETMWL) and Set Max Read Length (SETMRL)?** 

`1289` Implementers may choose to support any minimum value for these parameters, based on the Target’s use case `1290` and the supported I3C content protocol. This overrides any restrictions in previous versions of the I3C `1291` Specifications. Implementers may also require that a Target supports any value within the valid range; `1292` alternately, Implementers may also allow a Target to reject certain unsupported values within an otherwise `1293` valid range (i.e., not applying the change and returning the previous value unchanged on the next use of `1294` GETMWL or GETMRL). This allows for I3C content protocols that support byte streaming (i.e., access to a `1295` simple buffer or FIFO) as well as structured data messages with mandatory minimum lengths and other `1296` overall length requirements (i.e., incremental counts of structures with fixed or variable size). 

- `1297` • In version 1.0 of the I3C Specification, the minimum value for SETMWL was 8 bytes, and the `1298` minimum value for SETMRL was 16 bytes. 

- `1299` • In version 1.1 and later of the I3C Specification, the minimum value for SETMWL was changed `1300` to 16 bytes. 

- `1301` • Additionally, the GETMRL was previously defined to return a value of 0 for a value that was less `1302` than 16 bytes. 

`1303` All such restrictions (i.e., those listed above) are now removed. 

## **Q18.19 Do the configured Max Write Length and Max Read Length values apply to HDR Modes?** 

`1304` In general, yes. The intent for the SETMWL and SETMRL CCCs was to set the maximum transfer lengths `1305` in bytes of meaningful data, without regard to the specific I3C Mode or the Multi-Lane data transfer coding `1306` (if applicable). However, many HDR Modes require data bytes to be sent in structured protocol elements `1307` (such as Words or Blocks) that hold multiple bytes, where partial data elements are not allowed. Some HDR `1308` Modes may require the sender to insert padding bytes when there are not enough meaningful bytes to fill the `1309` last data element in a transfer; others might allow the sender to truncate the last data element in the transfer, `1310` subject to HDR Mode specific conditions. 

`1311` If the Target supports SETMWL and/or SETMRL and also allows the Controller to configure a maximum `1312` transfer length that is not an integer multiple of the data element size (i.e., the total number of data bytes in `1313` the Word/Block), then the Target must interpret the configured maximum transfer length for the meaningful `1314` data, and account for any padding bytes beyond the last meaningful data byte. `1315` For example: 

- `1316` • **In HDR-DDR Mode:** Each Data Word holds 2 bytes. If the configured maximum transfer length is `1317` an odd number of bytes (i.e., is not an integer multiple of 2 bytes), then: 

- `1318` • If the transfer length from the sender is the maximum, then the sender must add a padding byte `1319` in the last Data Word, and then compute the CRC in the CRC Word based on the entire transfer `1320` (including the last padding byte). 

- `1321` • The receiver will process all Data Words and ignore the padding byte, since the number of `1322` meaningful data bytes cannot be larger than the maximum transfer length. 

- `1323` • Similarly, if the transfer length from the sender is less than the maximum, then the sender would `1324` conditionally add a padding byte in the last Data Word, if the transfer has an odd number of `1325` meaningful bytes. The CRC in the CRC Word will be computed for the entire transfer (including `1326` a possible last padding byte). 

- `1327` • The receiver will process all Data Words and determine which bytes are valid based on the `1328` I3C content protocol; in other words, the receiver must determine whether any padding bytes `1329` are present. 

Copyright © 2018–2022 MIPI Alliance, Inc. 

39 

**Public Release Edition** 

FAQ for MIPI I3C v1.1.1 & MIPI I3C Basic v1.1.1 

FAQ Version 1.1 22-Aug-2022 

- `1330` • **In HDR-BT Mode:** Each Data Block holds 32 data bytes, but the Last Data Block may hold fewer `1331` data bytes. If the configured maximum transfer length is not an integer multiple of 32 bytes, then: 

- `1332` • The sender will indicate how many valid data bytes are in the Last Data Block, using the `1333` **Transition_Control** byte, and will provide padding bytes as needed. The sender will use a `1334` sufficient number of Data Blocks to hold the valid data bytes as well as the required padding. 

- `1335` • The CRC in the CRC Block will be computed based on the valid data bytes in the transfer, but `1336` not the padding bytes in the Last Data Block. 

- `1337` • The receiver will process all Data Blocks that are received, and will explicitly know which bytes `1338` in the Last Data Block are valid. 

`1339` _**Note:**_ 

`1340` _The appropriate value for padding bytes may vary, per each I3C Mode and particular Multi-Lane data_ `1341` _transfer coding (if applicable)._ 

`1342` Implementers that support maximum transfer lengths should account for these implications, for transfer `1343` lengths that are not an integer multiple of HDR Mode data elements. An I3C Device should be able to handle `1344` incoming HDR Mode transfers and determine whether any padding bytes are present, based on the HDR `1345` Mode framing, the particular I3C content protocol and the meaning of write/read transfers to/from an I3C `1346` Target. However, this may require that the I3C Device is able to receive a sufficient number of data elements `1347` (i.e., Words/Blocks) even if these data elements could potentially hold a larger total number of bytes (i.e., `1348` due to the required padding bytes). 

```
1349
```

## _**Note:**_ 

`1350` _Per_ _**Section 5.1.9.2.2** , I3C Controller and Target Devices shall ignore any additional, unrecognized_ `1351` _data bytes in CCC data payloads. Each standard CCC has its own defined data payload format._ 

## **Q18.20 How does the Target respond to the GETSTATUS CCC if the Controller sends ENEC/DISEC CCCs to enable or disable In-Band Interrupts?** 

`1352` If the Target supports In-Band Interrupts, then the GETSTATUS Format 1 response should still indicate `1353` whether any interrupts are pending (i.e., are waiting to be sent on the Bus as IBI Requests). 

`1354` The Controller can use the ENEC and DISEC CCCs to enable or disable IBI Requests (per specification `1355` _**Section 5.1.9.3.1**_ ), however this only affects the Target’s ability to send a pending interrupt via an IBI `1356` Request. If the Controller uses the DISEC CCC with the DISINT bit set, then the Target should still indicate `1357` whether it has any pending interrupts in Bits 3:0 of the GETSTATUS Format 1 response, regardless of `1358` whether IBI Requests are enabled or disabled. 

## **Q18.21 In the DEFTGTS CCC data bytes, where are the padding bits for the Controller’s Addresses?** 

`1359` The data bytes for Addresses, the Controller’s Dynamic Address, and the Controller’s Static Address (7’h7E) `1360` are in Bits[7:1], with Bit[0] used a padding bit with value 1’b0. This is the same format used for the `1361` subsequent data bytes that describe the Target and Group Addresses, as well as for other CCCs (such as `1362` SETDASA and SETNEWDA). 

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

40 

FAQ Version 1.1 22-Aug-2022 

FAQ for MIPI I3C v1.1.1 & MIPI I3C Basic v1.1.1 

## **2.19 High Data Rate (HDR) Modes** 

## **Q19.1 Does Figure 44 HDR-DDR Format apply for Command, Data, and CRC? Or only for Data?** 

`1363` _**Note:**_ 

`1364` _This question does not apply to I3C Basic v1.0._ 

`1365` Only for Data. The Data bytes are sent the same way as in SDR Mode. _**Figure 1**_ shows how Data is transferred `1366` from memory to the I3C Data Line. 

`1367` 

`1368` 

`1369` 

## **Figure 1 Data DWORDs sent as SDR Data Bytes and HDR-DDR Data Words** 

`1370` The Command and CRC Byte are each transferred as a packet instead: 

`1371` **Command** (MSb to LSb): 

- `1372` • Preamble (2 bits) 

- `1373` • Command (8 bits) 

- `1374` • Target address (7 bits) 

- `1375` • Reserved bit (1 bit) 

`1376` **CRC** (MSb to LSb): 

- `1377` • Preamble (2 bits) 

- `1378` • Token (4 bits) 

- `1379` • CRC Byte (5 bits) 

- `1380` • Setup bits (2 bits) 

`1381` _**Note:**_ 

`1382` _I3C Basic v1.1.1 and I3C v1.1+ already clarify the HDR-DDR protocol and coding details._ 

## **Q19.2 Does the Controller provide an additional CLK after the Terminate Condition and before the Restart/Exit Pattern, as shown in Figure 52 Controller Terminates Read?** 

`1383` _**Note:**_ 

`1384` _This question does not apply to I3C Basic v1.0._ 

`1385` No, there is an error in the I3C v1.0 specification’s _**Figure 52**_ . The beginning of the Restart/Exit Pattern `1386` should show SCL Low and SDA changing. This error was corrected in the I3C v1.1 specification and `1387` subsequent versions. 

## **Q19.3 During HDR-DDR Mode CRC 5 transmission, how many clocks should the Target expect to receive?** 

`1388` 

## _**Note:**_ 

`1389` _This question does not apply to I3C Basic v1.0._ 

`1390` The CRC transmission ends at bit 6 (counting down from bit 15), but bit 5 allows High-Z. 

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

41 

FAQ for MIPI I3C v1.1.1 & MIPI I3C Basic v1.1.1 

FAQ Version 1.1 22-Aug-2022 

## **Q19.4 For HDR-DDR Mode transfers, how should the Controller manage the Pull-Ups at the end of the HDR-DDR Command Word?** 

`1391` _**Note:**_ 

`1392` _This question does not apply to I3C Basic v1.0._ 

`1393` Per _**Q21.3**_ and _**Q21.4**_ , the Controller manages its Pull-Ups to allow for ACK/NACK as well as Bus `1394` Turnaround. The Controller sends the HDR-DDR Command Word with SDA in Active drive (i.e., Push-Pull `1395` mode) for the Command Word until the last Parity bit (i.e., PA0), which is initially driven High. Before the `1396` falling edge of C10 cycle, the Controller prepares for the Target to respond by disabling Push-Pull mode and `1397` engaging an appropriate Pull-Up to keep SDA at High. After the rising edge of the next C1 cycle, the `1398` addressed Target has the opportunity to either: 

- `1399` • Accept the DDR Write or Read by pulling SDA to Low, or 

- `1400` • Ignore the DDR Write or Read by leaving SDA at High (see also _**Q19.5**_ ) 

`1401` _**Note:**_ 

`1402` _This scheme is similar to SDR Mode’s ACK/NACK scheme for the Address Header, where SDA is_ `1403` _“Parked” at High and the Target can pull SDA to Low to acknowledge the transaction._ 

`1404` The Controller should use the appropriate Pull-Up to enable Bus Turnaround or acceptance by the Target. `1405` For most use cases, the Open-Drain class Pull-Up is recommended; however, the High-Keeper could also be `1406` used, based on system design factors per specification _**Section 5.1.3.1**_ . In either case, the Target must be able `1407` to pull SDA to Low before the falling edge of the C1 cycle. 

`1408` Note that the next C1 cycle is the start of the first HDR-DDR Data Word (if the Target accepts the transfer) `1409` and the PRE1 bit (i.e., the rising edge of the C1 cycle) is always 1’b1 per _**Section 5.2.2**_ . Using this scheme, `1410` the Target’s response determines the preamble bits: 

- `1411` • Bits 2’b10 indicate a Target ACK (i.e., accepting the DDR Write or Read) which starts the first `1412` HDR-DDR Data Word; or 

- `1413` • Bits 2’b11 indicate a Target NACK (i.e., ignoring the DDR Write or Read). The Controller then `1414` drives the HDR Restart Pattern or HDR Exit Pattern. 

## **Q19.5 In HDR-DDR Mode, how do Controllers and Targets enable flow control for NACK?** 

## `1415` _**Note:**_ 

- `1416` _This question does not apply to I3C Basic v1.0._ 

`1417` In I3C v1.0, HDR-DDR Mode did not define a flow control mechanism for a Target to actively deny (i.e., to `1418` NACK) a DDR Write Command. This meant that Targets had to ignore a DDR Write Command that they did `1419` not support (i.e., if the provided value of the HDR Command Byte was not supported), and the Controller `1420` would send the Data Words regardless. In such a situation, the Controller would proceed with the DDR Write `1421` and the Target would ignore all the Data Words (i.e., would take no action). 

`1422` In I3C v1.1 and later, HDR-DDR Mode added a mechanism for a Controller to configure a Target to either `1423` ignore the DDR Write Command, or else use an ACK/NACK mechanism similar to SDR Mode (see _**Q19.4**_ `1424` All Targets that comply with I3C v1.1 or newer are required to support this ACK/NACK mechanism, as well `1425` as the method of configuration from the Controller. Configuration is accomplished by using the ENDXFER `1426` CCC (see _**Section 5.1.9.3.25**_ ). 

`1427` The flow control diagram in _**Section 5.2.2**_ (i.e., _**Figure 128 HDR-DDR Preamble Bits State Diagram**_ ) shows 

`1428` how the suitably configured Target can provide NACK for a DDR Write Command, by providing a 1’b1 `1429` during the second preamble bit (i.e., before the first Data Word). In effect, Preamble value 2’b11 means that `1430` the Target has provided a NACK to the Controller; if the Controller sees this, then it must drive either the `1431` HDR Restart Pattern or the HDR Exit Pattern. By contrast, Preamble value 2’b10 means that the Target has `1432` pulled SDA Low and accepted the DDR Write Command (i.e., has provided ACK). _**Section 5.2.2.3.1**_ defines `1433` the ACK and NACK procedures in greater detail. The Controller must also ensure that the Target’s response `1434` is received: this typically requires the Controller to use a suitable delay in order to achieve proper set-up `1435` timing on the SDA line. 

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

42 

FAQ Version 1.1 22-Aug-2022 

FAQ for MIPI I3C v1.1.1 & MIPI I3C Basic v1.1.1 

## `1436` _**Note:**_ 

- `1437` 

- `1438` 

- `1439` 

```
1440
```

_If the Controller does not configure the Target to use the ACK/NACK capability for DDR Write Commands, then (A) the Target ignores the Data Words for any DDR Write Commands that it does not support; and (B) the Controller always drives Preamble value 2’b10 for the first Data Word, since it knows that the Target will ignore any DDR Write Commands that it does not support._ 

## **Q19.6 What has changed regarding HDR Modes in I3C v1.1.1?** 

## `1441` _**Note:**_ 

`1442` _This question does not apply to I3C Basic._ 

- `1443` In I3C v1.1 and earlier, the flow for transitioning from ENTHDRx CCCs into HDR Modes was not fully `1444` defined. I3C v1.1.1 fully defines the flow for transitioning from such CCCs into the first transfer in an HDR `1445` Mode, as well as the corresponding flow transitions from the HDR Restart Pattern to the next HDR transfer `1446` in the same HDR Mode. 

## **Q19.7 What has changed regarding HDR Ternary Modes in I3C v1.1.1?** 

## `1447` _**Note:**_ 

- `1448` _This question does not apply to I3C Basic._ 

- `1449` In addition to the changes regarding ENDXFER and HDR Ternary Flow Control (see _**Q18.16**_ ), I3C v1.1.1 `1450` now includes: 

- `1451` • Clarifications on the use of Group Addresses for Direct CCC Read/Write segments in HDR `1452` Ternary Modes 

- `1453` • Configuration advisories regarding use of common HDR Ternary Flow Control with CCCs, `1454` especially when sending Direct CCCs to Group Addresses. 

- `1455` • Clarification to the Option 2 End of CCC Procedure, which is now similar to starting a new CCC: `1456` all I3C Targets must acknowledge the Write Command to the Broadcast Address before the `1457` Controller sends an HDR Restart Pattern to end the CCC modality and return to generic HDR `1458` Ternary Read/Write commands. 

## **Q19.8 What has changed regarding HDR-BT Mode in I3C v1.1.1?** 

`1459` In addition to the Multi-Lane changes for HDR-BT Mode (see _**Q18.17**_ ), specification _**Section 5.2.4**_ now adds: 

- `1460` • Definitions on how to compute the Parity bits in the HDR-BT Header Block 

- `1461` • Definitions and examples for the CRC-16 and CRC-32 polynomials as used for HDR-BT CRC `1462` Block checksums 

- `1463` • Clarifications on how the HDR-BT CRC checksum values are calculated based on the data for `1464` each HDR-BT transfer 

- `1465` • Correction of an error in the figure showing Direct CCC flows in HDR-BT Mode 

- `1466` • Clarifications on the use of Group Addresses for Direct CCC Read/Write segments in HDR-BT `1467` Mode 

- `1468` • Correction of a specification error concerning the use of HDR-BT CRC Blocks in CCC Flows in `1469` HDR-BT Mode 

- `1470` • Clarifications to the **Transition_Verify** byte in the HDR-BT CRC Block; Bits[4:2] are now `1471` redefined as always zero 

- `1472` • Added new figures in specification _**Section 5.2.4.6**_ showing the Single-Lane format for all HDR- `1473` BT Mode structured protocol elements 

- `1474` • Corrections to the Dual-Lane and Quad-Lane figures for the HDR-BT Mode structured protocol `1475` elements, to resolve inconsistencies with the normative text and to show proper SDA Lane bit `1476` packing (i.e., the **Transition** , **Transition_Control** , and **Transition_Verify** bytes) 

- `1477` • Detailed explanation of the Data Block Delay mechanism (formerly called the Stall [delay] `1478` mechanism), which allows an I3C Target to delay sending the next HDR-BT Data Block until it `1479` has collected enough data bytes (see _**Q19.10**_ ) 

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

43 

FAQ for MIPI I3C v1.1.1 & MIPI I3C Basic v1.1.1 

FAQ Version 1.1 22-Aug-2022 

- `1480` • Better explanations of HDR-BT flow control details, including a new _**Section 5.2.4.7**_ with `1481` example HDR-BT transfers with different actions at the flow control points (i.e., the various `1482` **Transition** bytes) 

## **Q19.9 Are there any issues with the HDR-BT diagrams?** 

`1483` Yes. In the I3C v1.1 specification, _**Figure 164 CRC Block for Dual Lane and Quad Lane**_ (i.e., the HDR- `1484` BT CRC Block) presented the Dual Lane encoding of the CRC Block inaccurately, specifically in the `1485` _**Transition_Verify**_ byte: 

- `1486` • For HDR-BT Read transfers where the Target provides the clock, the figure incorrectly indicated `1487` the “handoff” point (where the Controller resumes driving SCL) as the C12 falling edge, i.e., the `1488` very end of the **Transition_Verify** byte for Dual Lane. The text of specification _**Section 5.2.4.2**_ . `1489` and _**Section 5.2.4.3.3**_ , by contrast, correctly defines the “handoff” point for Dual-Lane as the `1490` second half-clock of the **Transition_Verify** byte, i.e., the C11 falling edge. 

- `1491` • _**Figure 164**_ also incorrectly showed that the SDA[0] Lane could optionally be High after the `1492` “Park1, High-Z” on the C11\ clock cycle (i.e., Bits 4 and 6). The specification text, by contrast, `1493` correctly defines Bits[7:2] of the **Transition_Verify** byte as reserved, and requires them to be set to `1494` 0. In I3C v1.1.1, the specification text now defines Bits[4:2] as always 0, with Bits[7:5] still `1495` reserved for future definition by the MIPI I3C WG. 

- `1496` In both points above the v1.1 specification normative text was correct, and the Dual Lane HDR-BT CRC `1497` Block in _**Figure 164**_ was incorrect. The “handoff” point is indeed at the C11 falling edge, not the C12 falling `1498` edge. The I3C v1.1.1 specification clarifies these details and corrects the figure. Additionally, SDA[0] must `1499` be driven Low for Bit 4, even if the receiver does not drive SDA[0] Low and inform the transmitter that the `1500` CRC did not match after the “Park1, High-Z” (i.e., for the C11 falling edge). 

- `1501` _**Note:**_ 

- `1502` _For a Read transfer where the Target was providing clock, the “handoff” is required to occur before_ `1503` _the transmitter (i.e., the Target providing Read data) completes transmission of the_ _**Transition_Verify**_ `1504` _byte. In this case, the Target must then follow the Controller’s clock, since the Controller would drive_ `1505` _SCL after the falling edge of C11._ 

- `1506` _**Figure 2**_ shows a corrected version of the relevant details for the Dual Lane HDR-BT CRC Block, focusing `1507` on the **Transition_Verify** byte. The figure includes a portion of _**Figure 175**_ from the I3C v1.1.1 specification `1508` (see _**Section 5.2.4.6**_ ), highlighting the changes and clarifications. 

```
1509
```

**==> picture [427 x 204] intentionally omitted <==**

**----- Start of picture text -----**<br>
Previous definition in<br>I3C v1.1 Specification<br>showed that SDA[0]<br>CRC BLOCK<br>could remain High if<br>transfer was not<br>... CRC 3 TRANSITION_VERIFY<br>verified, now corrected<br>CRC3 CRC3 CRC3 CRC3 TRANS TRANS TRANS TRANS For Read transfers:<br>SDA[1]<br>[1] [3] [5] [7] [2] [3] [5] [7]<br>If Target drives SCL,<br>handoff occurs with<br>High Z of SDA[0], then<br>SDA[0] CRC3 CRC3 CRC3 CRC3 Park 1 High-Z TRANS TRANS Controller drives SCL<br>[0] [2] [4] [6] [4] [6] falling edge (C11)<br>Continue directly to<br>HDR Exit Pattern or<br>SCL C9 C10 C11 C12 HDR Restart Pattern<br>Incorrect Read handoff<br>location, as shown in<br>I3C v1.1 Specification<br>**----- End of picture text -----**<br>


**Figure 2 Corrected Figure 164, CRC Block for Dual Lane** 

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

44 

FAQ Version 1.1 22-Aug-2022 

FAQ for MIPI I3C v1.1.1 & MIPI I3C Basic v1.1.1 

## `1510` _**Note:**_ 

`1511` _The I3C v1.1.1 specification provides clarifications and improves the descriptions of the requirements_ `1512` _for handling the_ _**Transition_Verify** byte at the end of the CRC Block, for all defined Multi-Lane_ `1513` _configurations, including cases where the receiver fails to acknowledge the transfer. In general, the_ `1514` _Controller must control SDA[0] and any other SDA[1:3] data Lanes (per the Lane configuration) due_ `1515` _to the updated definition of the bit fields in the_ _**Transition_Verify** byte._ 

## **Q19.10 What is the HDR-BT Data Block Delay mechanism?** 

- `1516` This mechanism allows an I3C Target to delay sending a complete HDR-BT Data Block during an HDR-BT `1517` Read transfer, for situations where the I3C Target or its inner system was unable to fully prepare enough data `1518` bytes to fill a Data Block as part of the Read transfer in HDR-BT Mode. 

- `1519` In I3C v1.1, the HDR-BT Data Block Delay mechanism was called the “Stall (delay) mechanism” and was `1520` not fully defined. Additionally, the name “Stall (delay)” was too easily confused with other I3C defined `1521` behaviors in which SCL clock stalling is permitted (i.e., stalling by the I3C Controller is allowed, but never `1522` stalling by an I3C Target). The confusion occurred because this HDR-BT mechanism is fundamentally `1523` different from SDR Mode SCL clock stalling, and I3C forbids SCL clock stalling in HDR-BT Mode 

`1524` The I3C v1.1.1 specification addresses this confusion by renaming the mechanism to more accurately reflect `1525` its definition, and by adding clearer, more complete normative details. In addition, the name of parameter `1526` “tBT_STALL” was changed to “tBT_DBD”. 

`1527` During an HDR-BT Read transfer, the Data Block Delay mechanism allows the I3C Target to transmit either: 

- `1528` • A valid Data Block, which is not intended to be the last such Data Block, if the Target has a full 32 `1529` bytes of data to transmit; or 

- `1530` • A single Delay byte, indicating that the Target is not yet ready to transmit a Data Block and that `1531` the I3C Controller should therefore continue the Read if it wishes to receive more data. 

- `1532` This Delay byte differs from a valid **Transition_Control** byte (i.e., the first byte of an HDR-BT Data Block). `1533` The I3C Target may defer sending a Data Block (i.e., by sending a Delay byte up to a maximum of 1024 `1534` times) at any point of a Read transfer, before it must terminate the Read transfer. The I3C Controller also has `1535` the opportunity either to continue waiting (i.e., receiving more Delay bytes until the I3C Target has enough `1536` data), or to terminate the Read transfer at its discretion. 

- `1537` This mechanism does not allow an I3C Target to delay sending either the CRC Block or the Last Data Block `1538` (e.g., one that might have “ragged” data). 

- `1539` The I3C Controller determines whether the I3C Target may use the Data Byte Delay mechanism. The `1540` Controller indicates this in the Control byte of the HDR-BT Header Block that starts each HDR-BT Read `1541` transfer. 

- `1542` • If the I3C Target supports this mechanism and chooses to use it for this transfer, then the Target `1543` may use the mechanism if needed. 

- `1544` • If the I3C Target does not support this mechanism, or if the I3C Controller has indicated that the `1545` Data Byte Delay is not permitted, then the I3C Target must not use this mechanism, in case it `1546` encountered a situation where it was unable to fully prepare enough bytes to fill a Data Block. In `1547` such a situation, the I3C Target might be forced to end the HDR-BT Read transfer early (i.e., by `1548` sending incomplete data). 

- `1549` This mechanism is primarily useful when the I3C Controller controls the SCL clock during the HDR-BT `1550` Read transfer, as the I3C Target would otherwise not have a method for indicating that the transfer should be `1551` slowed to match the actual rate of Data Blocks that it can reasonably produce (i.e., from its inner system that `1552` might provide the data bytes). 

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

45 

FAQ for MIPI I3C v1.1.1 & MIPI I3C Basic v1.1.1 

FAQ Version 1.1 22-Aug-2022 

## **2.20 I3C Advanced Capabilities** 

## **Q20.1 What is Offline, and what does it mean to be Offline Capable?** 

`1553` The Offline capability allows a Target to become inactive on the I3C Bus at some times, but then return to `1554` normal activity later. The Offline capability is now indicated in the Target’s Bus Control Register (BCR). `1555` Offline-capable Targets indicate this capability with BCR Bit[3] set to 1'b1. 

`1556` An Offline-capable Target can become inactive on the I3C Bus, but some portion of the Target will still `1557` monitor the Bus either for Target Reset, or for the use of the Target’s Dynamic Address. The monitoring `1558` portion of the Target retains the Target’s Dynamic Address, even though the Target might be mostly `1559` powered‑off or in deepest sleep. 

`1560` While offline, such Targets can be awakened (i.e., can be re‑activated) by a Target Reset or by the use of their `1561` Dynamic Address. They will take some time to become active on the Bus again, such as the RSTACT CCC `1562` recovery from Full Reset time. While they are offline, and while awakening, these Targets will not be `1563` responsive to the Controller, nor will they record CCCs, nor will they necessarily retain state (e.g., the `1564` ENEC/DISEC CCCs); as a result, the Controller will have to wait until such Targets become active, and then `1565` might also need to configure them again. This is all by private contract (agreement). 

`1566` See specification _**Section 5.1.10.2.5**_ for details, both in I3C v1.0 (which does not include Target Reset) and `1567` in I3C v1.1 (which does include Target Reset). 

`1568` _**Note:**_ 

```
1569
```

```
1570
```

```
1571
1572
```

_Offline-capable Targets are required to preserve their Dynamic Addresses as long as they are powered. A Target that can become fully inactive on the I3C Bus and lose its Dynamic Address will subsequently Hot-Join to get a new Dynamic Address; such a Target is not considered to be an Offline-capable Target, and it must set BCR Bit[3] to 1’b0._ 

## **Q20.2 What is a Virtual Target?** 

`1573` Generally, a Virtual Target is a function of a single physical Device that represents multiple I3C Targets on `1574` the I3C Bus, such that the I3C Controller can address each of those Targets independently. 

`1575` In the simplest form, a Virtual Target could be one of a set of several Target Devices, all integrated into the `1576` same physical package and all sharing a common set of pins connecting them to an I3C Bus. 

`1577` In a more advanced form, a Virtual Target could act as one of several virtualized functions presented by a `1578` highly-integrated Device that stores a different Dynamic Address for each function. Depending on the `1579` implementation, such virtualized functions might share configuration information, and might return the same `1580` values for some CCCs. 

`1581` Examples could include Bridging or Routing Devices, as well as other types of Devices that expose multiple `1582` functions and use shared Peripheral logic. I3C v1.1 defines several new capabilities and features for such `1583` Virtual Targets. 

`1584` For details, see the I3C Specification at _**Section 5.1.9.3.19**_ , and the _**I3C Application Note: General Topics**_ `1585` _**[MIPI05]**_ at _**Section 5.7**_ . 

## **Q20.3 Does the I3C Bus support Bridges?** 

`1586` Yes. Bridge Devices enable an I3C Bus to be bridged to other protocols, such as SPI, UART, etc. The `1587` SETBRGTGT (Set Bridge Target) CCC is defined to enable Bridge Devices, where the Controller either `1588` knows in advance that certain Devices are bridges, or can discover a Bridge Device during Bus initialization. 

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

46 

FAQ Version 1.1 22-Aug-2022 

FAQ for MIPI I3C v1.1.1 & MIPI I3C Basic v1.1.1 

## **Q20.4 How does the Set Bridge Targets (SETBRGTGT) CCC differ between I3C v1.0 and I3C v1.1+?** 

- `1589` In I3C v1.1, use of this CCC is expanded to support Bridging Devices that have Dynamic Addresses, which `1590` makes multiple Bridging Devices on the same I3C Bus possible. The context of the SETBRGTGT CCC is `1591` also redefined: a Bridging Device is now one of several types of Devices that expose or present Virtual `1592` Targets. Bit[4] of the Target’s Bus Configuration Register (BCR) now indicates Virtual Target capabilities. 

- `1593` For bridged Targets that are enabled by a Bridging Device, I3C v1.1 clarifies the use of other CCCs (such as `1594` SETMRL) that address a bridged Target. The I3C v1.1 specification also clarifies that to change the Dynamic `1595` Address of a bridged Target, the SETBRGTGT CCC (not the SETNEWDA CCC) must be used. 

- `1596` For details, see the I3C Specification at _**Sections 5.1.1.2.1**_ , _**5.1.9.3.17**_ , and _**5.1.9.3.19**_ . 

## **Q20.5 Does the I3C Bus enable Routing?** 

`1597` Yes. I3C v1.1+ and I3C Basic v1.1.1 define the requirements, expectations, and configuration for Routing `1598` Devices. 

- `1599` Routing Devices enable the creation of multiple Routes across I3C Buses. A Routing Device enables more `1600` advanced Bus topologies, and requires buffers or queues to handle transactions across each Route. 

- `1601` A Routing Device contains a Control Function which is presented on the I3C Bus as a Virtual Target. The `1602` Controller configures the Routing Device by sending the SETROUTE CCC to its Control Function. Routes `1603` to other I3C Buses are treated as downstream targets, each of which generally has a Target Function which `1604` is also presented as a Virtual Target with its own Dynamic Address. Transactions are sent to the Route’s 

- `1605` Target Function via its Dynamic Address, and the Routing Device manages the communications on the `1606` downstream I3C Bus. 

```
1607
```

For details, see the I3C Specification at _**Section 5.1.9.3.20**_ . 

## **Q20.6 Why does I3C allow more than one Controller on the I3C Bus? What can a Secondary Controller do that the Primary Controller can’t?** 

`1608` The system designer decides whether their system needs more than one Controller on the Bus. To provide `1609` that flexibility MIPI I3C allows this, but also does not require it. Controller Role Handoff is a well-defined `1610` and controlled mechanism in I3C; if used, it can be relied on. 

- `1611` For most use cases, a Secondary Controller is not a required component for an I3C Bus. If your Primary `1612` Controller has all the capabilities and features that you need, and if your use of the I3C Bus wouldn’t benefit `1613` from having multiple Controller-capable Devices, then you might not need a Secondary Controller. 

- `1614` 

- `1615` 

Examples where Secondary Controllers are useful: 

   1. A Debug controller, if present, would be a Secondary Controller 

- `1616` 2. A sensor hub or other offload device can be used to continue operating during periods when the `1617` Host processor is in deep sleep (i.e., to save power) 

- `1618` 3. The system can switch between standalone use (such as IoT devices) and connected uses. For `1619` example, perhaps a USB-to-I3C cable is attached to take over temporarily. 

- `1620` Note that Devices such as MCUs will usually be able to operate as fully-fledged Targets, as fully-fledged `1621` Primary Controllers, and as Secondary Controllers (i.e., Devices that come up as Targets but can become the `1622` Active Controller later), depending solely on the particular needs of the given system. They can simply be `1623` configured for the Bus they are on by the firmware. 

- `1624` 

## _**Note:**_ 

`1625` _This FAQ entry has been updated for I3C v1.1.1 and I3C Basic v1.1.1. In this FAQ entry, the terms_ `1626` _“Primary Controller” and “Secondary Controller” refer to an I3C Device’s initial configuration and_ `1627` _capabilities. In other sections of this FAQ and the I3C specification, the term “Secondary Controller”_ `1628` _might instead reflect a Controller-capable Device’s current role, i.e., as and when it is not currently_ `1629` _the “Active Controller” of the Bus. See_ _**Q13.4** for additional details._ 

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

47 

FAQ for MIPI I3C v1.1.1 & MIPI I3C Basic v1.1.1 

FAQ Version 1.1 22-Aug-2022 

## **Q20.7 Is any time-stamping capability defined for the I3C Bus?** 

`1630` _**Note:**_ 

- `1631` • _This question does not apply to I3C Basic v1.0._ 

- `1632` • _I3C Basic v1.1.1 only supports Timing Control with Async Mode 0._ 

`1633` Yes. The I3C Bus supports an optional Timing Control mechanism which has multiple timing modes. One `1634` timing mode is synchronous (from the synchronized timing reference) and four modes are asynchronous `1635` (Target provides timestamp data). All I3C Controllers are expected to support at least Async Mode 0. 

- `1636` • **Synchronous:** The Controller emits a periodic time sync that allows Targets to set their sampling `1637` time relative to this sync. This may be used in conjunction with one of the Asynchronous modes. 

- `1638` • **Asynchronous:** The Targets apply their own timestamps to the data at the time they acquire `1639` samples, permitting the Controller to time-correlate samples received from multiple different `1640` Targets or sensors. 

- `1641` There are four types (timing modes) of asynchronous time controls: 

- `1642` • **Async Mode 0:** Basic timing mode that assumes that a Target has access to a reasonably `1643` accurate and stable clock source to drive the time stamping – at least accurate for the duration of `1644` the time it has to measure (i.e., from event to IBI). A set of counters, in conjunction with IBI, are `1645` used to communicate time stamping information to the Controller. 

- `1646` • **Async Mode 1:** Advanced timing mode extends the Basic mode by using some mutually `1647` identifiable Bus events, like I3C START. 

- `1648` • **Async Mode 2:** High-precision timing mode that uses SCL falling edges (for SDR and HDR- `1649` DDR modes) as a common timing reference for Controller and Target. A burst oscillator is used `1650` to interpolate the time between a detected event and next SCL falling edge. For HDR-TSL and `1651` HDR-TSP modes, this timing mode uses both SDA transitions and SCL transitions as timing `1652` references. 

- `1653` • **Async Mode 3:** Highest-precision triggerable timing mode that supports precise time triggering `1654` and measurement across multiple transducers applications like beam forming. 

   - **Q20.8 Can Synchronous and Asynchronous Timing Control both be enabled at the same time?** 

```
1655
```

## _**Note:**_ 

`1656` _This question does not apply to I3C Basic v1.0._ 

`1657` Yes. This is allowed such that the ODR (Output Data Rate) rate controls the In-Band Interrupt (IBI) rate, and `1658` the Async Mode timestamp on the IBI indicates how long ago the sample was collected. 

## **Q20.9 Is there a way to turn off Timing Control?** 

```
1659
```

## _**Note:**_ 

`1660` _This question does not apply to I3C Basic v1.0._ 

`1661` Yes, the Controller can turn off Timing Control by sending the SETXTIME CCC with the value 0xFF in the `1662` Sub-Command byte. 

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

48 

FAQ Version 1.1 22-Aug-2022 

FAQ for MIPI I3C v1.1.1 & MIPI I3C Basic v1.1.1 

## **Q20.10 What has changed regarding Multi-Lane for SDR Mode?** 

`1663` _**Note:**_ 

`1664` _This question does not apply to I3C Basic v1.0._ 

`1665` In I3C v1.1, the Data Transfer Codings for Multi-Lane in SDR Mode (SDR-ML) define the Header Byte to `1666` contain supplementary information to be sent on SDA[1] (i.e., the first Additional Data Lane) when `1667` Multi-Lane is enabled for SDR Mode. This supplementary information includes the inverse of the Address, `1668` since the Header Byte was defined to include the I3C Address Header and was intended to be received and `1669` understood by existing I3C Targets that did not necessarily support SDR-ML. 

`1670` Upon review, the I3C WG realized that this method would cause implementation challenges during an `1671` Arbitrable Address Header (i.e., after a START) if the I3C Controller were required to echo any changes it `1672` saw on SDA[0] (i.e., to track changes that an I3C Target might drive during Address Arbitration) when `1673` emitting the inverse on SDA[1]. The I3C v1.1.1 specification address these issues by changing the definition `1674` of the Header Byte for SDR-ML to only require the I3C Controller to send this supplementary information `1675` on SDA[1] for the Header Byte (i.e., an Address Header) after a Repeated START. When sending the Header `1676` Byte after a START, the I3C Controller is now required to keep SDA[1] and any other Data Lanes in a High-Z `1677` state, rather than driving this supplementary information. 

`1678` In SDR Mode, CCCs are always sent in 1-Lane mode, allowing all I3C Targets to track the Command Code `1679` and Defining Byte (if any) in the CCC Framing. This rule places limitations on the use of SDR-ML: 

- `1680` 1. If SDR-ML is used, then the Targets should not rely on supplementary information on SDA[1] for `1681` the Header Byte (i.e., the Address Header); the supplemental information should be treated as `1682` optional, because 1-Lane Targets (i.e., Targets that might not support SDR-ML) must track CCC `1683` framing and flow elements but can only see SDA[0]. 

- `1684` 2. Transfers after a Repeated START that comprise Broadcast CCCs (i.e., transfers addressed to `1685` 7’h7E) must also be sent only in SDR 1-Lane mode. As a result, SDR-ML cannot be used for `1686` Broadcast CCCs in SDR Mode. 

- `1687` 3. Transfers after a Repeated START that comprise CCC flow elements (e.g., Direct CCC segments `1688` addressed to a specific Target or Group) must only be sent in SDR 1-Lane mode. As a result, `1689` SDR-ML also cannot be used for Direct CCCs in SDR Mode. 

`1690` Conditions #2 and #3 above are especially relevant because both Broadcast CCCs and Direct CCCs may be `1691` mixed in among Private Write/Read transfers in continuous SDR Mode framing (i.e., without intervening `1692` STOP Conditions). In such cases the Controller should not send the supplementary information during the `1693` Address Header, and Targets supporting SDR-ML are required not to depend on it, because they will know `1694` that the Controller is sending a CCC. Furthermore, the Controller must not use SDR-ML data byte encoding `1695` for CCCs (both Broadcast and Direct) because some Targets on the I3C Bus might not understand the `1696` encoding. 

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

49 

FAQ for MIPI I3C v1.1.1 & MIPI I3C Basic v1.1.1 

FAQ Version 1.1 22-Aug-2022 

## **2.21 Electricals and Signaling** 

## **Q21.1 How many signal lines does I3C have?** 

```
1697
```

I3C has two mandatory signal lines: Data (SDA) and Clock (SCL). 

`1698` I3C v1.1+ and I3C Basic v1.1.1 also support optional Multi-Lane transfers, which use additional Data lines `1699` for supported I3C Modes. In Multi-Lane, the SDA line is called SDA[0] and the additional data lines are `1700` called SDA[1], SDA[2], etc. 

## **Q21.2 Does I3C require Pull-Up resistors on the bus like I²C?** 

`1701` Not necessarily. I3C Controllers manage an active (i.e., dynamic) Pull-Up resistance on SDA, which they `1702` can enable and disable as the Bus transitions between Open Drain and Push-Pull mode. This might be a `1703` board-level resistor that is switchable (i.e., that can be engaged/disengaged as needed, controlled by an output `1704` pin from the Controller), or internal to the Controller, or any combination of the two. 

- `1705` _**Note:**_ 

`1706` _If an I3C Bus has multiple Controller-capable Devices (i.e., one Active Controller and one or more_ `1707` _Secondary Controllers), then the Active Controller manages the Pull-Up on SDA._ 

## **Q21.3 When is the Pull-Up resistor enabled?** 

`1708` In order to achieve higher data rates, much of the activity on the I3C Bus occurs in Push-Pull mode (i.e., with `1709` the Open Drain Pull-Up resistor disabled). 

- `1710` However for some Bus management activities, and for backwards compatibility with I[2] C, Pull-Up-resistor- `1711` based Open Drain mode is enabled. Examples include: 

- `1712` • Arbitration during Dynamic Address Assignment 

- `1713` • Address Header following a START, which is arbitrable and can become an In-Band Interrupt `1714` Request 

- `1715` • ACK/NACK during the 9[th] bit of an Address Header. 

`1716` With very few exceptions, the I3C Controller is responsible for providing an Open Drain class Pull-Up `1717` resistor when the Bus is in the Open Drain mode. See specification _**Section 5.1.3.1**_ . 

- `1718` _**Note:**_ 

`1719` _The Open Drain class Pull-Up for SDA could either be provided internally by the Controller, or it could_ `1720` _be an external device that is engaged or disengaged as needed, i.e., switchable between these_ `1721` _states and controlled by a Controller output pin._ 

`1722` _By contrast, SCL should always be driven by the Active Controller (i.e., Push-Pull) and no Open Drain_ `1723` _class Pull-Up is needed._ 

## **Q21.4 Is a High-Keeper needed for the I3C Bus?** 

`1724` A High-Keeper is used for Controller-to-Target and Target-to-Controller Bus handoff, as well as optionally `1725` when the Bus is idle (see _**Q22.1**_ ). The High-Keeper may be a passive weak Pull-Up resistor on the Bus, or an `1726` active weak Pull-Up (or equivalent) in the Controller. The High-Keeper is only required to be strong enough `1727` to prevent system-leakage from pulling the Bus Low. At the same time, the High-Keeper for the SDA line `1728` must be weak enough that a Target with the minimum IOL driver can pull the SDA line Low within the **trDA** `1729` minimum period. The system designer is responsible for balancing these factors. 

- `1730` _**Note:**_ 

```
1731
```

```
1732
```

```
1733
1734
1735
1736
```

_A High-Keeper is required for both SDA and SCL. External High-Keepers might be required if the Active Controller’s High-Keeper is not adequate per specification_ _**Section 5.1.3.1** . Additionally, if an I3C Bus has multiple Controller-capable Devices (i.e., one Primary Controller and one or more Secondary Controllers), then the Active Controller is responsible for managing the High-Keeper, and Controllers using the Controller Role Handoff Procedure are required to engage or disengage their High-Keepers at the defined times during this procedure (per_ _**Section 5.1.7.2** )._ 

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

50 

FAQ Version 1.1 22-Aug-2022 

FAQ for MIPI I3C v1.1.1 & MIPI I3C Basic v1.1.1 

## **2.22 Bus Conditions and States** 

## **Q22.1 What are some of the I3C Bus conditions when the Bus is considered inactive?** 

`1737` In addition to Open-Drain, Pull-Up, and High-Keeper, the I3C Bus has three distinct conditions under which `1738` the Bus is considered inactive: Bus Free, Bus Available, and Bus Idle. 

- `1739` • **Bus Free** condition is defined as a period occurring after a STOP and before a START and for a `1740` given duration (e.g., tCAS and tBUF timing). 

- `1741` • **Bus Available** condition is defined as a Bus Free condition with duration of at least tAVAL. A Target `1742` may only issue a START request (e.g., for In-Band Interrupt or Controller Handoff) after a Bus `1743` Available condition. 

- `1744` • **Bus Idle** condition is defined to help ensure Bus stability during Hot-Join events. This condition is `1745` defined as a period during which the Bus Available condition is sustained continuously for a `1746` duration of at least tIDLE. 

## **Q22.2 When an I3C Device wishes to send an In-Band Interrupt (IBI) Request, does it need to see a STOP before a Bus Idle?** 

- `1747` For normal active I3C Targets, yes. They should only send an In-Band Interrupt (IBI) Request when they `1748` have seen a STOP and the tAVAL time has elapsed (about 1 µs), and in response to a START (but not a `1749` Repeated START). 

- `1750` For Hot-Joining Devices using the standard Hot-Join method, they do not necessarily know the Bus condition, `1751` so they wait until the Bus is Idle (i.e., until SCL and SDA are both high for a duration of at least tIDLE). 

## **Q22.3 When can an I3C Target issue an In-Band Interrupt (IBI) Request?** 

- `1752` An I3C Target can issue the IBI in the following two ways: 

- `1753` • Following a START (but not a Repeated START) 

- `1754` • If no START is forthcoming within the Bus Available condition, then an I3C Target can issue a `1755` START request by pulling the SDA line Low. The I3C Controller would then complete the START `1756` condition by pulling the SCL clock line Low and taking over the SDA line. 

## **Q22.4 What are the I3C Bus Activity States?** 

- `1757` Bus Activity States provide a mechanism for the Controller to inform the Targets about the expected `1758` upcoming levels of activity or inactivity on the Bus, in order to help Targets better manage their internal `1759` states (e.g., to save power). 

- `1760` There are four Bus Activity States, each with an expected activity interval: 

- `1761` • **Activity State 0:** Normal activity 

- `1762` • **Activity State 1:** Expect quiet for at least 100 µs 

- `1763` • **Activity State 2:** Expect quiet for at least 2 ms 

- `1764` • **Activity State 3:** Expect quiet for at least 50 ms 

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

51 

FAQ for MIPI I3C v1.1.1 & MIPI I3C Basic v1.1.1 

FAQ Version 1.1 22-Aug-2022 

## **2.23 Resets and Error Handling** 

## **Q23.1 Are there any test modes in the I3C Bus?** 

```
1765
```

```
1766
```

```
1767
```

```
1768
```

```
1769
```

Yes. The Directed and Broadcast ENTTM CCCs (see specification _**Section 5.1.9.3.8**_ ) allow the Controller to enter and exit the test modes. Support for the ENTTM CCC is optional for I3C Targets. 

The I3C v1.1+ and I3C Basic v1.1.1 specifications also define an optional Defining Byte for the GETCAPS CCC: the Read Fixed Test Pattern command (see specification _**Section 5.1.9.3.19**_ ). This provides simple Bus testing that can be supported by I3C Controllers and Targets. 

## **Q23.2 Are there any error detection and recovery methods in I3C?** 

```
1770
```

```
1771
```

```
1772
```

Yes, the I3C Bus has elaborate error detection and recovery methods. Seven Target error types (TE0 through TE6) and four Controller error types (CE0 through CE3) are defined for SDR Mode, along with suggested recovery methods. In addition, a similar set of errors is defined for each HDR Mode. 

`1773` _**Note:**_ 

`1774` _This question has been updated for I3C v1.1+ and I3C Basic v1.1.1. These versions add new Error_ `1775` _Types CE3 and DBR._ 

## **Q23.3 What happens if the Controller crashes during a Read?** 

`1776` An I3C Target may optionally choose to time out if it detects more than 100 µs without an SCL edge (see `1777` specification _**Section 5.1.2.3**_ ). If that happens, the Target can abandon the Read and release SDA to avoid a `1778` Bus hang when the Controller restarts. 

`1779` The optional timeout of 100 µs with no SCL activity is a recommended minimum. It does not have to be `1780` precise, but since I3C’s minimum frequency is 10 KHz, anything longer than 100 µs means that the `1781` Controller has failed to complete the Read, so the Target should High-Z the SDA line and abandon the Read. 

`1782` _**Note:**_ 

```
1783
```

```
1784
```

```
1785
```

_If the Target is in Legacy I[2] C mode, then it would not normally abandon the read, since there is no minimum frequency, and because 9 clocks by a Controller will be enough to abort the Read (since the 9th bit of data is ACK/NACK for a Read in Legacy I[2] C Mode)._ 

## **Q23.4 Is there any way to exit from an Error of Type TE0 or TE1, other than waiting for an Exit Pattern?** 

`1786` Yes. An I3C Target may optionally watch for 60 µs with no SCL or SDA changes to make sure that the Bus `1787` is not in HDR Mode (and therefore must be in SDR Mode). After that, it is appropriate to wait for START `1788` (assumed to be Repeated START) or STOP. 

## **Q23.5 Can a Controller issue a STOP condition regardless of whether or not a Target has issued an acknowledgment indicating a completed transaction?** 

`1789` The STOP can be issued anywhere the Target is not driving the SDA during SCL High. It may not be `1790` appropriate to do so in terms of completion of a message. But ACK and completed transaction do not belong `1791` together in I3C. 

## **Q23.6 What errors are reported on the GETSTATUS Protocol Error bit?** 

`1792` The Protocol Error Report bit on the GETSTATUS CCC is intended to report errors that have no other way `1793` of being detected unless the Device reports them. It is intended to cover parity error, CRC error, and anything `1794` else that means that a message from the Controller was lost and the Controller has no way of knowing it. 

`1795` The Protocol Error Report on the GETSTATUS CCC would not cover the case of TE5 errors, as they are `1796` more related to an unsupported CCC or Defining Byte (which is not a protocol error _per se_ ). It is also not `1797` intended for situations when the Target NACKs, because the Controller will know that an error occurred `1798` when the Target NACKs and recovers it. Errors such as Error Types TE0, TE3, TE4, and TE5 are detected `1799` by the Controller when the Target sends a NACK response, and are recovered by using the appropriate `1800` recovery methods; as a result, they need not be reported via the GETSTATUS CCC. 

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

52 

FAQ Version 1.1 22-Aug-2022 

FAQ for MIPI I3C v1.1.1 & MIPI I3C Basic v1.1.1 

## **Q23.7 What errors does Target Error Type TE5 cover?** 

`1801` Error Type TE5 covers illegally formatted CCCs that an I3C Target might see on the I3C Bus. 

- `1802` Due to confusion around the use of the words “illegally formatted” in the I3C v1.0 specification, I3C v1.1 `1803` more precisely defined what errors are considered to be instances of Error Type TE5. This section covers `1804` only four cases of errors, as follows. 

- `1805` • The first two cases listed in I3C v1.1 are Unsupported Command Codes and Unsupported `1806` Defining Bytes (i.e., for a supported Command Code), both of which are ignored by a Target if not `1807` supported. 

- `1808` Note that these are not strictly “illegally formatted” CCCs _per se_ according to v1.1.1’s clarified `1809` definition of Error Type TE5, since the CCC format itself might be correct (if the Target happened `1810` to support that CCC). Nonetheless, a Target must still NACK any Command Code or Defining `1811` Byte that it does not support, so that the Controller will see the NACK and know that the Target is `1812` unable to respond to the CCC. In cases where these commands have a special exit condition, the `1813` Target should also still wait for the applicable exit condition. 

- `1814` • The two cases addressed by Error Type TE5 are when the Controller sends the wrong RnW Bit for `1815` a Direct CCC command. That is, the Controller sends a Dynamic Address and Read bit for a `1816` Direct Write or Direct SET CCC command, or vice versa. In these cases, the Target must NACK `1817` its Address, thus notifying the Controller that an error has occurred. The Controller will then use `1818` the Retry and Escalation models. 

- `1819` Additional Defining Bytes, or Additional Data on CCC Payloads, are not error conditions. Targets should `1820` ignore any additional unrecognized data bytes, per the specification at _**Section 5.1.9.2.2**_ . 

- `1821` _**Note:**_ 

- `1822` _In previous versions of I3C and I3C Basic, Error Type TE5 was named Error Type S5; see_ _**Q5.2** for_ `1823` _name change details._ 

## **Q23.8 Are Devices required to wait for a Repeated START or STOP, or both, to recover from Error Types TE2–TE5?** 

- `1824` Error Types TE2 through TE5 should be recovered by STOP. 

- `1825` However: 

- `1826` • **Error Types TE2, TE3, and TE5:** Vendors may optionally elect to have Devices recover from `1827` these Error Types upon seeing a Repeated START, per the transaction type. 

- `1828` • For these Error Types that support optional Repeated START recovery, STOP is the second step `1829` of escalation after Repeated START recovery. 

- `1830` • If Error Types TE2 and TE5 are seen during a Direct CCC, then the Target must retain the CCC `1831` state until the Target detects the end of the CCC (i.e., the end of the modality). Since the `1832` Controller uses the Direct CCC framing model, the CCC modality will continue until the `1833` Controller sends either STOP, or Repeated START with 7’h7E (see specification `1834` _**Section 5.1.9.1**_ ). 

- `1835` • If the Controller simply uses a Repeated START (without 7’h7E) and stays in the Direct CCC `1836` framing model, then the Target must remember that the CCC modality is still active, and must `1837` treat the subsequent transfer as a Direct CCC, not a Private Read/Write. 

- `1838` • Note that Broadcast CCCs do not require Repeated START with 7’h7E to end the CCC `1839` modality: these end with a simple Repeated START (i.e., no 7’h7E is needed). 

- `1840` • If I3C Devices are not sure whether Repeated START recovery is appropriate for a situation, `1841` then it is safer to ignore subsequent CCCs in the SDR Frame and wait for STOP. 

- `1842` • **Error Type TE4:** Requires STOP recovery (the Repeated START option does not apply). 

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

53 

FAQ for MIPI I3C v1.1.1 & MIPI I3C Basic v1.1.1 

FAQ Version 1.1 22-Aug-2022 

## **Q23.9 What has changed regarding Target Error Types in I3C v1.1.1?** 

`1843` **Error Type TE0** (formerly named Error Type S0; see specification _**Section 5.1.10.1.1**_ ) now more clearly `1844` defines the I3C Target Address restrictions for an I3C Controller, and explains the single-bit error conditions `1845` that might occur if the restricted Addresses were used. 

- `1846` **Error Type TE5** (formerly named Error Type S5; see _**Section 5.1.10.1.6**_ ) now only provides examples of `1847` “illegally formatted” CCCs that include an incorrect RnW bit for a Direct CCC. Error Type TE5 no longer `1848` lists unsupported CCCs as an error case (see _**Q23.7**_ ). 

- `1849` Note that the Target requirements for handling an unsupported Command Code or unsupported `1850` Defining Byte are now defined in specification _**Section 5.1.9.2.2**_ . Although these cases are not `1851` strictly covered by Error Type TE5, a Controller might interpret a Target’s NACK response `1852` similarly and handle it with the same recovery procedure. 

- `1853` **Error Type TE6** (formerly named Error Type S6; see _**Section 5.1.10.1.7**_ ) now clearly defines the difference `1854` between the Target’s response to a CCC that it perceives as a Read (i.e., a Direct GET or a Direct Read) when `1855` there is an error in the RnW bit. This better explains the way that the Target should handle the error situation, `1856` i.e., when the Controller actually intended to send a Write (i.e., a Direct SET or a Direct Write). 

## **Q23.10 When does the RSTACT CCC state clear in an I3C Target?** 

- `1857` The RSTACT state will be cleared back to default upon either: 

- `1858` 

   1. Detection of a Target Reset Pattern. This will enact the RSTACT action, and then clear the state. 

- `1859` 2. Detection of a completed START (but not repeated START). The RSTACT may be cleared either `1860` on that falling edge, or on the rising edge that follows. 

## **Q23.11 What is the minimal Target Reset support required in I3C v1.1 or v1.1.1?** 

`1861` I3C Targets that comply with I3C v1.1+ or I3C v1.1.1 must support the Target Reset Pattern, and at least the `1862` Peripheral Reset action (i.e., RSTACT CCC with Defining Byte 0x01). 

`1863` Although MIPI Alliance strongly recommends true support of Target Reset, such that a Controller can fully `1864` reset a Target chip when needed, it is not required. Full/Chip Reset (see specification _**Section 5.1.11.4**_ ) allows `1865` replacement of a dedicated pin that would normally be used to reset a Device. 

- `1866` _**Note:**_ 

`1867` _If supported, a Full/Chip Reset causes a typical I3C Target to return to its power-on configuration,_ `1868` _which means re-enabling its I[2] C Spike Filter if it has one. If so, then the I3C Controller must tell the_ `1869` _I3C Target to turn off its Spike Filter again (see_ _**Q24.1** )._ 

`1870` The minimal reset is a reset of the I3C peripheral, at least to a level that will allow a ‘stuck’ I3C peripheral `1871` to start working again. How much of a reset that requires is up to the Target vendor; for example, it could be `1872` handled by an internal interrupt which would allow firmware/software in the Target to handle the reset. 

## **Q23.12 When does a Target escalate Target Reset to Full/Chip Reset?** 

`1873` If the Target does not receive a RSTACT CCC before seeing the Target Reset Pattern, then it uses the default `1874` action of Peripheral Reset: it resets just the I3C block. If the Target again receives no RSTACT CCC before `1875` seeing a Target Reset, it then escalates to a Full/Chip Reset. It therefore retains the state after any default `1876` Peripheral Reset, so it can then activate the escalation. This state is cleared if the Target sees either an `1877` RSTACT CCC, or a GETSTATUS CCC addressed to it. 

`1878` _**Note:**_ 

```
1879
```

```
1880
```

```
1881
```

```
1882
1883
1884
```

_The purpose of this mechanism is to fix a broken system or setup. Because the Target Reset Pattern Detector logic is normally separated both from the I3C block and from other parts of the main system, it will continue to work even if the rest of the chip becomes broken (e.g., clocks stopped, Bus locked up, etc.). This means that not seeing a RSTACT CCC would be a symptom of a large problem, so the Target escalates in order to recover from such a broken condition. The Target first performs a Peripheral Reset, in case the fault condition exists only in the I3C block itself._ 

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

54 

FAQ Version 1.1 22-Aug-2022 

FAQ for MIPI I3C v1.1.1 & MIPI I3C Basic v1.1.1 

## **Q23.13 How is Target escalation affected when the RSTACT CCC is received?** 

`1885` The RSTACT CCC only determines how the Target will interpret the next Target Reset Pattern that it receives, `1886` the RSTACT CCC does not alter the handling of any currently in-progress Target escalation. 

- `1887` For this reason: 

- `1888` • A Device that supports the RSTACT CCC should always prioritize RSTACT configuration over `1889` any currently occurring Target escalation. 

- `1890` • Any Target escalation operation that might be in progress when the RSTACT CCC is received `1891` should be cleared. 

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

55 

FAQ for MIPI I3C v1.1.1 & MIPI I3C Basic v1.1.1 

FAQ Version 1.1 22-Aug-2022 

## **2.24 Timing Parameters** 

## **Q24.1 Are there any special timing requirements for sending the first START with the Broadcast Address?** 

`1892` Yes. The I3C Controller must emit the first START with the Broadcast Address (7’h7E) at Open-Drain speeds `1893` (i.e., usually I[2] C Fm+ timings) so that I3C Targets with I[2] C Spike Filters (per _**Q15.4**_ ) will be able to see the `1894` I3C Broadcast Address, and then as a result turn off the Spike Filter (per the specification at `1895` _**Section 5.1.2.1.1**_ ). 

- `1896` 

## _**Note:**_ 

- `1897` _If another I3C Target arbitrates its own Address (or the special reserved address for a Hot-Join_ `1898` _Request) into this Address Header and thereby wins arbitration, then the I3C Controller must repeat_ `1899` _this special Address Header._ 

- `1900` _If such an I3C Target supports Full/Chip Reset using the Target Reset Pattern (which might be_ `1901` _preceded by the RSTACT CCC; see specification_ _**Section 5.1.11.4** ), then it will most likely re-enable_ `1902` _its I[2] C Spike Filter after such a Full/Chip Reset. In this case, the I3C Controller must emit the START_ `1903` _condition with the Broadcast Address (7’h7E) at Open-Drain speeds again, so that the I3C Target_ `1904` _can turn off the Spike Filter._ 

`1905` However, if the Controller knows that none of the I3C Targets has a Spike Filter, then it may omit this. `1906` Similarly, if the Controller knows that all of the I3C Targets have accurate Spike Filters, then it may use the `1907` I3C 2.5 MHz Open-Drain speed (i.e., 200 ns Low, 200 ns High). 

## **Q24.2 What is the I3C Open-Drain tHigh Max? Table 10 shows it as 41 ns, but a Note says it may be longer** 

`1908` In the I3C v1.1 specification, _**Table 110 I3C Open Draining Timing Parameters**_ shows the tHigh symbol `1909` maximum value as 41 ns, and Note 4 states “tHigh may be exceeded when the signals can be safely seen by `1910` I[2] C Targets”. This means that a 41 ns tHigh will ensure that no Legacy I[2] C Target will see the SCL changes, `1911` and so no Legacy I[2] C Target will interpret the START followed by the Address phase nor the ACK/NACK. `1912` If there is no harm with a Legacy I[2] C Target on the I3C Bus seeing the clocks, then the Controller may use a `1913` much longer tHigh. For example, Legacy I[2] C Targets will see the STOP and then a START. It is acceptable for `1914` them to see the Address that follows (arbitrated or not), since none of those Addresses will match their own `1915` Address. However, as the tLow may well be 200 ns, this may present problems for any Legacy I[2] C Targets not `1916` fast enough to correctly handle a 200 ns Low period. 

`1917` In the I3C v1.1.1 specification, the parameters are defined in the equivalent _**Table 122**_ . In the I3C Basic `1918` v1.1.1 specification, the parameters are defined in the equivalent _**Table 86**_ . 

## **Q24.3 How should tSCO timing be interpreted?** 

```
1919
```

This is extensively covered in the I3C v1.1+ and I3C Basic v1.1.1 specifications at _**Section 5.1.9.3.18**_ . 

## **Q24.4 If a Device has a tSCO value greater than 12 ns, does that mean it doesn’t qualify as an I3C Device?** 

```
1920
```

- `1921` 

## _**Note:**_ 

_This question does not apply to I3C Basic v1.0._ 

`1922` No. The tSCO (Clock-to-Data Turnaround delay time) parameter is information provided by Target Devices `1923` so that system designers can properly compute the maximum effective frequency for reads on the Bus. The `1924` tSCO number is meant to be used together with the line capacitance (trace length) and number of Targets and `1925` stubs (if present). 

- `1926` However, I3C Targets with tSCO delay greater than 12 ns must do all of the following: 

- `1927` • Set the Limitation bit in the Bus Characteristics Register (BCR) to 1’b1 

```
1928
```

   - Set the Clock-to-Data Turnaround field of the maxRD Byte to 3’b111 

- `1929` • Communicate the tSCO value to the Controller by private agreement (i.e., product datasheet) 

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

56 

FAQ Version 1.1 22-Aug-2022 

FAQ for MIPI I3C v1.1.1 & MIPI I3C Basic v1.1.1 

`1930` _**Note:**_ 

`1931` _I3C Basic v1.0 and I3C v1.1+ already clarify these aspects of communications in I3C._ 

## **Q24.5 How do tCBSr and tCASr timing differ between I3C v1.1 and I3C v1.0?** 

`1932` In I3C v1.0, parameter tCASr’s minimum value was tCASmin. In I3C v1.1, this was reduced to tCASmin/2. Since `1933` satisfying this reduced duration might be challenging for some Targets, the Controller is required to provide `1934` suitable timing, i.e., is required to accommodate the slowest Devices on the Bus. 

`1935` In version 1.1 of the I3C specification, a new Note clarifying this point was added to _**Table 111 I3C Push-**_ `1936` _**Pull Timing Parameters for SDR, ML, HDR-DDR, and HDR-BT Modes**_ (in _**Section 6.2**_ ): 

`1937` _9) Targets with speed limitations inform the Controller via the Bus Characteristics Register (BCR)_ `1938` _that the minimum may not be acceptable. As a result, if the given SCL HIGH period is 50 ns or greater,_ `1939` _then the Controller needs to accommodate for Legacy I[2] C Devices that might see it._ 

`1940` In the I3C v1.1.1 specification, this Note appears in the equivalent _**Table 123**_ . In the I3C Basic v1.1.1 `1941` specification, it appears in the equivalent _**Table 87**_ . 

## **Q24.6 Are there any special timing parameters for sending the HDR Exit Pattern, HDR Restart Pattern or Target Reset Pattern?** 

`1942` Yes. The I3C Controller must always observe the minimum timing requirements for all of these defined `1943` patterns. _**Section 6.2**_ defines the minimum value of parameter **tDIG_H** for such transitions, and this is `1944` mentioned explicitly in _**Section 5.2.1.1.1**_ (i.e., for the HDR Exit Pattern). 

`1945` Since the HDR Restart Pattern and the Target Reset Pattern are both based on the HDR Exit Pattern, the same `1946` timing parameters apply to all patterns. Note that the Controller may send all such patterns at slower clock `1947` speeds if needed, as long as each transition on SDA and/or SCL observes the minimum value parameter `1948` **tDIG_H** . 

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

57 

FAQ for MIPI I3C v1.1.1 & MIPI I3C Basic v1.1.1 

FAQ Version 1.1 22-Aug-2022 

## **3 Terminology** 

`1949` See also _**Section 2**_ in the MIPI I3C Specification _**[MIPI01][MIPI09][MIPI11]**_ 

## **3.1 Definitions** 

- `1950` **Bus Available:** I3C Bus condition in which a Device is able to initiate a transaction on the Bus. 

- `1951` **Bus Free:** I3C Bus condition after a STOP and before a START with a duration of at least tCAS. 

- `1952` **Bus Idle:** An extended duration of the Bus Free condition, during which Devices may attempt to Hot-Join `1953` the I3C Bus. 

- `1954` **Controller:** The I3C Bus Device that is controlling the Bus. (I3C and I3C Basic versions prior to v1.1.1 used `1955` the deprecated term Master.) 

- `1956` **High-Keeper:** A weak Pull-Up type Device used when SDA, and sometimes SCL, is in High-Z with respect `1957` to all Devices. 

- `1958` **Hot-Join:** Targets that join the I3C Bus after it is already started, whether because they were not powered 

- `1959` previously or because they were physically inserted into the Bus. The Hot-Join mechanism allows the Target `1960` to notify the Controller that it is ready to get a Dynamic Address. 

- `1961` **In-Band Interrupt (IBI):** A method whereby a Target Device emits its Address into the arbitrated Address `1962` header on the I3C Bus to notify the Controller of an interrupt. 

- `1963` 

   - **Master:** Deprecated term used in I3C and I3C Basic versions prior to v1.1.1. See Controller. 

- `1964` **Primary Controller:** Controller-capable Device that has initial control of the I3C Bus. Formerly called `1965` “Main Master”. 

- `1966` **Slave:** Deprecated term used in I3C and I3C Basic versions prior to v1.1.1. See Target. 

- `1967` **Target:** An I3C Target Device can only respond to either Common or individual commands from a Controller. `1968` (I3C and I3C Basic versions prior to v1.1.1 used the deprecated term Slave.) 

## **3.2 Abbreviations** 

`1969` ACK Short for “acknowledge” (an I3C Bus operation) 

- `1970` DisCo Discovery and Configuration (family of MIPI Alliance interface specifications) 

- `1971` e.g. For example (Latin: exempli gratia) 

- `1972` i.e. That is (Latin: id est) 

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

58 

FAQ Version 1.1 22-Aug-2022 

FAQ for MIPI I3C v1.1.1 & MIPI I3C Basic v1.1.1 

## **3.3 Acronyms** 

- `1973` See also the acronyms defined in the MIPI I3C Specification _**[MIPI01][MIPI09][MIPI11]**_ . `1974` CCC Common Command Code (an I3C common command or its unique code number) `1975` CTS Conformance Test Suite `1976` DAA Dynamic Address Assignment (an I3C Bus operation) `1977` FAQ Frequently Asked Questions `1978` HCI Host Controller Interface (a MIPI Alliance interface specification _**[MIPI02][MIPI12]**_ ) `1979` HDR High Data Rate (a set of I3C Bus Modes) `1980` HDR-BT HDR Bulk Transfer (an I3C Bus Mode) `1981` HDR-DDR HDR Double Data Rate (an I3C Bus Mode) `1982` HDR-TSL HDR Ternary Symbol Legacy (an I3C Bus Mode) `1983` HDR-TSP HDR Ternary Symbol for Pure Bus (an I3C Bus Mode) `1984` I3C Improved Inter Integrated Circuit (a MIPI Alliance interface specification `1985` _**[MIPI01][MIPI09][MIPI11]**_ ) `1986` IBI In-Band Interrupt (an I3C Bus feature) `1987` ML Multi-Lane (an I3C Bus feature, and set of Data Transfer Codings for I3C Bus Modes) `1988` ODR Output Data Rate `1989` SCL Serial Clock (an I3C Bus line) `1990` SDA Serial Data (an I3C Bus line) `1991` SDR Single Data Rate (an I3C Bus Mode) `1992` SPI Serial Peripheral Interface (an interface specification) 

Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

59 

FAQ for MIPI I3C v1.1.1 & MIPI I3C Basic v1.1.1 

FAQ Version 1.1 22-Aug-2022 

## **4 References** 

|`1993`|[MIPI01]|_MIPI Alliance Specification for I3C® (Improved Inter Integrated Circuit)_, version 1.0,|
|---|---|---|
|`1994`||MIPI Alliance, Inc., 23 December 2016 (Adopted 31 December 2016).|
|`1995`|[MIPI02]|_MIPI Alliance Specification for I3C Host Controller Interface (I3C HCISM)_, version 1.0,|
|`1996`||MIPI Alliance, Inc., 29 September 2017 (Adopted 4 April 2018).|
|`1997`|[MIPI03]|_MIPI Alliance Specification for Discovery and Configuration (DisCoSM)_, version 1.0,|
|`1998`||MIPI Alliance, Inc., 1 July 2016 (Adopted 28 December 2016).|
|`1999`|[MIPI04]|_MIPI Alliance DisCoSM Specification for I3CSM_, version 1.0, MIPI Alliance, Inc.,|
|`2000`||25 January 2019 (Adopted 18 June 2019).|
|`2001`|[MIPI05]|_MIPI Alliance I3C Application Note: General Topics_, App Note version 1.1,|
|`2002`||MIPI Alliance, Inc., In press.|
|`2003`|[MIPI06]|_MIPI Alliance Specification for Camera Serial Interface 2 (CSI-2SM_), version 4.0,|
|`2004`||MIPI Alliance, Inc., 26 September 2021 (Adopted 8 December 2021).|
|`2005`|[MIPI07]|_MIPI Alliance Specification for Debug for I3CSM_, version 1.0, MIPI Alliance, Inc.,|
|`2006`||21 April 2020 (Adopted 4 September 2020).|
|`2007`|[MIPI08]|_MIPI Alliance Conformance Test Suite (CTS) for I3CSM v1.1.1 and I3C Basic v1.1.1_,|
|`2008`||CTS version 1.0, MIPI Alliance, Inc., 4 August 2021 (approved 5 August 2021).|
|`2009`|[MIPI09]|_MIPI Alliance Specification for I3C BasicSM (Improved Inter Integrated Circuit)_,|
|`2010`||version 1.0, MIPI Alliance, Inc., 19 July 2018 (Adopted 8 October 2018).|
|`2011`|[MIPI10]|MIPI Alliance, Inc., “I3C SETBUSCON Table”,|
|`2012`||<https://www.mipi.org/MIPI_I3C_bus_context_byte_values_public.html>, last accessed|
|`2013`||22 August 2022.|
|`2014`|[MIPI11]|_MIPI Alliance Specification for I3C® (Improved Inter Integrated Circuit)_, version 1.1,|
|`2015`||MIPI Alliance, Inc., 27 November 2019 (Adopted 11 December 2019).|
|`2016`|[MIPI12]|_MIPI Alliance Specification for I3C Host Controller Interface (I3C HCISM)_, version 1.1,|
|`2017`||MIPI Alliance, Inc., 20 May 2021 (Adopted 20 May 2021).|
|`2018`|[MIPI13]|_MIPI Alliance Specification for I3C® (Improved Inter Integrated Circuit)_, version 1.1.1,|
|`2019`||MIPI Alliance, Inc., 11 June 2021 (Adopted 8 June 2021).|
|`2020`|[MIPI14]|_MIPI Alliance Specification for I3C BasicSM (Improved Inter Integrated Circuit)_,|
|`2021`||version 1.1.1, MIPI Alliance, Inc., 9 June 2021 (Adopted 21 July2021).|
|`2022`||**_Note:_**|
|`2023`||_Version number v1.1 was not used for I3C Basic._|
|`2024`|[MIPI15]|_MIPI Alliance Specification for Debug for I3CSM_, version 1.1, MIPI Alliance, Inc.,|
|`2025`||In press.|
|`2026`|[LINX01]|Linux Kernel Patches for I3C subsystem, <https://patchwork.kernel.org/project/linux-|
|`2027`||i3c/list/>, last accessed 22 August 2022.|



Copyright © 2018–2022 MIPI Alliance, Inc. **Public Release Edition** 

60 

