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
* _**[New!]**_ _**[HighLight!]**_ We have finished the TDoA method of PSK Audio Signal. Time difference between two paths is employed to measure the 1D distance. The theorical error is lower than 1 cm in our experiments. TDoA would be a critical part of out paper!
* _**[New!]**_ The distance measurement is almost the same to Alex Liu. L1=2.10cm, L2=11.95cm.

###Work on Track
* _**[New!]**_ Our devices only has one microphone. so We add an additional microphone on the top of the smartphon. It's not perfect. But it can work. After I analyse the Android source code, I find it's hard to use the different microphone to record different soundwave at the same device at the same time. There is a conflict inside the android. I will try it in the later days again..

###Work in plan
* _**[New!]**_ _**[HighLight!]**_ We would test it next Monday 11/14 night.

##OFDM Audio Signal
###Work Have Done
* We have research the topic of FDM and OFDM. FDM would be easy, OFDM is difficult but within better effect. Both of two methods would be tested in the next week. Then, we would decide which one to be used finally.

###Work in Track
* Shengjie would design the modulate-demodulate program this weekend.

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

Wish for a good luck in November.
