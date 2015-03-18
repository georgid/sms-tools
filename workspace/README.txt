workspace/harmonicModel_function has the main logic

-extractHarmSpec()
sets params for extarction and loads pitchSeries
for now it is hard coded to work with one particular audio.
TODO: load stereo as mono with MonoLoader
	
-resynthesize()


software.models.harmonicModel.harmonicModelAnal_2()
extracts harm elements from the spectrum (based on main melody provided)

software.models.harmonicModel.harmonicDetection()
 	when f0 detected but no peaks above threshold => return zero harmonics
 	
 -------------------------------------------------------
 mainLobeMatcher implements a technique of compariong shape of peaks to mainLobe of blackman-harris window
 
 see V. Rao and P. Rao - Vocal melody extraction in the presence of pitched accompaniment in polyphonic music, II.B
 
 code in workspace/mainLobeMatcher
 