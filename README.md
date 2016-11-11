# SWatchPad
Build the audio wireless tracking platform - SJTU Network Lab
Up till now, we have done following work

##PSK Audio Singnal and Processing
###Work Have Done
* We have modulated simple waves into PSK waves of 3 different frequency options 
* We have established both the hardware environment and software environment in smart phone.
* We have tested the playing and recording of the mobile phone. Now we can record the wav file and then analysis it.
* We completed the frequency analysis of PSK wave. It is found that the PSK wave donot change the frequency.
* _**[New!]**_ We have demodulated（解调） the audio signal into digital signal. The method used is 差分相干解调. NOt only the ideal wave passed the test, also the wave recorded by mobile phone passed the test. We now have a mature modulate-demodulate method.
* _**[New!]**_ We separates two different waves, one spreads from speaker to microhphone directly, and another one reflected by user's hand. The time difference is observed from the PSK demodulated result.
* _**[New!]**_ The hardware limitation has been researched. Now we use the major-mic and camera-mic. We still have some tech problems. If we can not overcome it. Then we would use the additional microhphone instead of the built-in mic.

###Work on Track
* _**[New!]**_ Shengjie would cover the 1D measuring problem this weekend. Since the Time Difference of Arrival Waves has been got from the PSK. Therefore, this measuring program would no longer be the problem.
* _**[New!]**_ Bo would cover the transformation from 1D distance to 2D distance. It is a solid geometry problem within sort of calculation. We predict it would be solved in this weekend.
* _**[New!]**_ Bo would continue the hardware improvement. The final hardware improvement would be determined in this weekend.

###Work in plan
* Most problems had been solved. We would test it next Monday 11/14.

##OFDM Audio Signal
###Work Have Done
* _**[New!]**_ We have research the topic of FDM and OFDM. FDM would be easy, OFDM is difficult but within better effect. Both of two methods would be tested in the next week. Then, we would decide which one to be used finally.
###Work in Track
* _**[New!]**_ Shengjie would design the modulate-demodulate program this weekend.
###Work in plan
Also the combination of PSK and usual wave is critical in our paper. The PSK told us the information of distance, 
and doppler effect of usual wave gave us the motion information.


##Double-Static Tracking
###Work in plan
Easy step if we get the PSK time difference.

##Single-Static-Single-Dynamic Tracking
###Work in plan
It would be major task in the next week.

##Double-Dynamic Tracking
###Work in plan
It would be mojor task in the next week as well.

Wish for a good luck in November.
