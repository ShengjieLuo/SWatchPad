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