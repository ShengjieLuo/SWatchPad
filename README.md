# SWatchPad
Build the audio wireless tracking platform - SJTU Network Lab

**Work Track in 11/13**

##PSK Audio Singnal and Processing
###Work Have Done
* We have modulated simple waves into PSK waves of 3 different frequency options 
* We have established both the hardware environment and software environment in smart phone.
* We have tested the playing and recording of the mobile phone. Now we can record the wav file and then analysis it.
* We completed the frequency analysis of PSK wave. It is found that the PSK wave donot change the frequency.
* We have demodulated（解调） the audio signal into digital signal. The method used is 差分相干解调. NOt only the ideal wave passed the test, also the wave recorded by mobile phone passed the test. We now have a mature modulate-demodulate method.
* We separates two different waves, one spreads from speaker to microhphone directly, and another one reflected by user's hand. The time difference is observed from the PSK demodulated result.
* _**[HighLight!]**_ We have finished the PSK-TDoA test. Time difference between two paths is employed to measure the 1D distance. The theorical error is lower than 1 cm in our experiments. We have designed a new algorithm for PSK method and improve the mathematical expression to enhance the measuring accuracy.
* We have finished the hardware environment setup. Now we use one speaker and one microphone of the smartphone. An additonal microphone is stick on the smartphone and used as the second built-in microhpone.
* We have finished the 1Dto2D function and passed the test.

###Work on Track
* _**[New!]**_ Shengjie would try to combine the ToA and TDoA if time if allowed. The accuracy currently measured can be accepted. We would do this task in the next stage. Now we would change to the next topic. 

###Work in plan
* _[NO work in plan now]_

##FDM Audio Signal
###Work Have Done
* We have research the topic of FDM and OFDM. FDM would be easy, OFDM is difficult but within better effect. Both of two methods would be tested in the next week. Then, we would decide which one to be used finally.
* _**[New!Highlight!]**_We have designed two tech plans, the first of which uses the Frequency Fliter and FDM, the othe of which uses FFT and IFFT. Both of methods would be tested in this stage.

###Work in Track
* _**[New!]**_ Bo would take charge of this step and write the program.
* _**[New!]**_ Shengjie would focus on Doppler effect these two days. The doppler effect program comes from the program we use in VPad.

###Work in plan
* The combination of PSK and usual wave is critical in our paper. The PSK told us the information of distance, 
and doppler effect of usual wave gave us the motion information.


##Static-Static Tracking
###Work in plan
Easy step if we get the PSK time difference.

##Static-Dynamic Tracking
###Work in plan
It would be major task in the next week.

##Dynamic-Dynamic Tracking
###Work in plan
It would be mojor task in the next week as well.

Wish a good luck for Chinese Football Team this night!
