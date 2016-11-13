#Hardware 

##
###Graph and describe

![Graph](./Device_outlooking.png)


*	Because our device only has one mic, we add a mic on the top of the device and receive the sound by computer.
To reduce the time delay between computer and smartphone, use some application to control the smartphone on computer.
I have tried to use the smartphone which has two mic, but failed. 
It's hard to use two microphones to record different sound at the same device at the same time
I will try it again in the later days.

# Difficulty in Android

##
###Our present android device

*	Our device only has one microphone

* Added an additional mircophone and computer will received the sound received by the additional microphone.

###Try to use two microphones at one device
*	Bo has tried and according to the bug log, there is a conflict inside the android. Usually we use the class AudioTrack to record the sound wave. We can use MediaRecorder.AudioSource.MIC or MediaRecorder.AudioSource.CAMCORDER as the source. They are major microphone and camera microphone. However We can't use them at the same time. 
*	This is the bug log： <MediaPlayer：Should have subtitle controller already set>
*	It means after we choose to use one microphone ,another microphone is not availiable because they share the same part of the code inside the class AudioTrack. Unfortunately, the source code is very difficult to understand.

###Way to overcome
* Bo will try to rewrite the Class AudioTrack and try other devices in the next week