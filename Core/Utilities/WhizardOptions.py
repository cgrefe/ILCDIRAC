'''
Created on Nov 3, 2011


For SUSY special treatment of the pythia parameters have to be thought of: if the model is SUSY, then need to add
IMSS(1)=11; IMSS(21)=71; IMSS(22)=71;

This is currently done on the job definition side
 
@author: Stephane Poss
'''

from xml.etree.ElementTree                                import ElementTree, fromstring
from ILCDIRAC.Core.Utilities.GeneratorModels              import GeneratorModels

import types

from DIRAC import S_OK, S_ERROR

def getDict():
  """ Get list of available fields in the whizard options.
  """
  pdict = {}
  pdict['process_input'] = {}
  pdict['integration_input'] = {}
  pdict['simulation_input'] = {}
  pdict['diagnostics_input'] = {}
  pdict['beam_input_1'] = {}
  pdict['beam_input_2'] = {}

  return S_OK(pdict)

class WhizardOptions(object):
  """ Class that provides an interface to the xml representation of the whizard options.
  """
  def __init__(self, model = "sm"):
    self.genmodel = GeneratorModels()
    self.paramdict = {}
    modelparams = self.modelParams(model)
    self.whizardxml = fromstring("""<whizard>
<process_input>
<process_id type="string" value="">
<!-- Process tag(s) as defined in whizard.prc. It should contain the list of processes to activate, separated by commas or blanks, enclosed in quotes. -->
</process_id>
<cm_frame type="T/F" value="T">
<!-- if true, the c.m. frame is the lab frame, the beams are in +/- z directions, and the total c.m. energy is given by sqrts. If false, the beam energies and directions must be specified below in the blocks beam_input. -->
</cm_frame>
<sqrts type="float" value="3000">
<!-- If this number is greater than the sum of the incoming particle masses, it specifies the c.m. energy of the initial state in GeV. Applies only if cm_frame is true, and is ignored for decay processes. -->
</sqrts>
<luminosity type="float" value="0">
<!-- Integrated luminosity in fb-1 -->
</luminosity>
<polarized_beams type="T/F" value="T">
<!-- If true, the helicity content of the beams must be specified below in the blocks beam_input. -->
</polarized_beams>
<structured_beams type="T/F" value="T">
<!-- If true, the nature of the incoming beams must be specified below in the blocks beam_input. -->
</structured_beams>
<beam_recoil type="T/F" value="F">
<!-- If true, and if structure functions (e.g., ISR) are selected, the recoil of the partons against the beam remnant (e.g., the emitted photons) is taken into account. The pT distribution is computed within the approximation valid for the emission, hence it will be accurate at low pT. -->
</beam_recoil>
<recoil_conserve_momentum type="T/F" value="F">
<!-- Applies only if beam_recoil is set: if true, keep momentum balance between parton and recoil momenta at the expense of energy balance. If false, keep energy balance at the expense of momentum balance. -->
</recoil_conserve_momentum>
<filename type="string" value="whizard">
<!-- Base filename (w/o extension) to be used for all input/output files instead of the string "whizard". -->
</filename>
<directory type="string" value="">
<!-- Working directory for all further reading/writing of files. -->
</directory>
<input_file type="string" value="">
<!-- If nonempty, read the specified input file after the current one. The extension .in will be appended to the filename. -->
</input_file>
<input_slha_format type="T/F" value="F">
<!-- If true, assume that the next input file is in SUSY Les Houches Accord format (see Sec. 4.4.7). If false, determine the format from the first line. -->
</input_slha_format>
</process_input>
<integration_input>
<calls type="floatarray" value="1 50000 10 50000 1 1500000">
<!-- Array describing the number of iterations and number of calls per integration pass. Default values depend on the selected process. See below in subsection 4.6 for details. -->
</calls>
<seed type="integer" value="">
<!-- Random number generator seed (integer). When omitted, the time counter will be used, resulting in a different value each run. -->
</seed>
<reset_seed_each_process type="T/F" value="F">
<!-- Reset the random number generator seed to seed not just once, but each time a process is integrated. This is useful for comparing matrix elements which should be identical, but, e.g., have been generated by different programs. -->
</reset_seed_each_process>
<accuracy_goal type="float" value="0">
<!-- Goal for the accuracy estimate (6th column in the output). When this goal is reached and the efficiency goal is either also reached or unset, further grid adaptation iterations will be skipped (Sec. 4.9). -->
</accuracy_goal>
<efficiency_goal type="float" value="100">
<!-- Goal for the reweighting efficiency estimate (7th column in the output). When this goal is reached and the accuracy goal is either also reached or unset, further grid adaptation iterations will be skipped (Sec. 4.9). -->
</efficiency_goal>
<time_limit_adaptation type="integer" value="0">
<!-- If nonzero, grid adaptation for the current process will be stopped after the specified number of minutes, and the final integration pass started (Sec. 4.9). -->
</time_limit_adaptation>
<stratified type="T/F" value="T">
<!-- Use stratified (T) / importance (F) sampling. -->
</stratified>
<use_efficiency type="T/F" value="F">
<!-- Use efficiency (T) / accuracy (F) as the criterion for adapting the channel weights. -->
</use_efficiency>
<weights_power type="float" value="0.25">
<!-- Power used for adapting the channel weights. Lower value means slower adaptation (to suppress fluctuations). -->
</weights_power>
<min_bins type="integer" value="3">
<!-- Minimal number of bins per integration dimension. -->
</min_bins>
<max_bins type="integer" value="20">
<!-- Maximal number of bins per integration dimension. This number will be used as long as there are enough sampling points, otherwise the number of bins will be decreased. -->
</max_bins>
<min_calls_per_bin type="integer" value="10">
<!-- Minimal number of points per bin, integration dimension, and integration channel. If this limit cannot be satisfied, the total number of points will be increased. -->
</min_calls_per_bin>
<min_calls_per_channel type="integer" value="0">
<!-- All integration channel will get at least (approximately) this number of points. Prevents channels from being dropped during adaptation. -->
</min_calls_per_channel>
<write_grids type="T/F" value="T">
<!-- Write grids to files whizard.grb (best grid) and whizard.grc (current grid), to be reused later. -->
</write_grids>
<write_grids_raw type="T/F" value="F">
<!-- Use binary format for writing grids. Saves memory at the expense of portability. -->
</write_grids_raw>
<write_grids_file type="string" value="">
<!-- If nonempty, use the specified filename for writing grids instead of the default. The file extensions are appended to string. -->
</write_grids_file>
<write_all_grids type="T/F" value="F">
<!-- Write, in addition, after each iteration the current grid to file whizard.grXXX, where XXX is the iteration number. -->
</write_all_grids>
<write_all_grids_file type="string" value="">
<!-- If nonempty, use the specified filename for writing the extra grids instead of the default. The file extensions are appended to string. -->
</write_all_grids_file>
<read_grids type="T/F" value="F">
<!-- Read existing grids whizard.grb and whizard.grc if they have been written by a previous run. This avoids the time-consuming adaptation step. Makes sense only if no physical parameters have been changed. -->
</read_grids>
<read_grids_raw type="T/F" value="F">
<!-- If true, search first for binary grid files, then for ASCII grids. If false, do search first for ASCII.. -->
</read_grids_raw>
<read_grids_force type="T/F" value="T">
<!-- Set this to T if you want to read the grids from file even if some parameters have changed. Use with care! This may result in a program crash if the grid structures are incompatible. -->
</read_grids_force>
<read_grids_file type="string" value="">
<!-- If nonempty, use the specified filename for reading grids instead of the default. The file extensions are appended to string. -->
</read_grids_file>
<generate_phase_space type="T/F" value="T">
<!-- Generate a phase space configuration appropriate for the current process and write it to whizard.phx. -->
</generate_phase_space>
<read_model_file type="string" value="">
<!-- If nonempty, read vertex definitions for phase space setup from string.mdl instead of the default whizard.mdl. -->
</read_model_file>
<write_phase_space_file type="string" value="">
<!-- Write phase space configuration to string.phx instead of the default. -->
</write_phase_space_file>
<read_phase_space type="T/F" value="T">
<!-- Read phase space configuration from whizard.phs or a previously generated file whizard.phx if possible. -->
</read_phase_space>
<read_phase_space_file type="string" value="">
<!-- Read phase space configuration from string.phs or string.phx instead of the default. -->
</read_phase_space_file>
<phase_space_only type="T/F" value="F">
<!-- Stop the program after phase space generation. -->
</phase_space_only>
<use_equivalences type="T/F" value="T">
<!-- If true, use permutation symmetry when updating grids to improve the quality of the results. -->
</use_equivalences>
<azimuthal_dependence type="T/F" value="F">
<!-- If false, it is assumed that the scattering does not depend on the overall azimuthal angle. This will be automatically T if general beam polarization is switched on, therefore the user need only access this parameter in the case of azimuthal-dependent cuts. -->
</azimuthal_dependence>
<write_phase_space_channels_file type="string" value="">
<!-- Show phase space channels in string.ps instead of the default file whizard-channels.ps. Note that you need to call CHANNELS= string make -e channels in order to generate string.ps -->
</write_phase_space_channels_file>
<off_shell_lines type="integer" value="1">
<!-- Maximum number of off-shell-lines allowed for Feynman graphs which are initially taken into account for the phase space configuration. Log-enhanced (massless) propagators are not counted as off-shell. -->
</off_shell_lines>
<extra_off_shell_lines type="integer" value="1">
<!-- Use configurations with more off-shell lines, if they happen to be maximally resonant. -->
</extra_off_shell_lines>
<splitting_depth type="integer" value="1">
<!-- Up to this number of branchings, a (massless) propagator will be considered as log-enhanced and mapped like a photon propagator. -->
</splitting_depth>
<exchange_lines type="integer" value="3">
<!-- Up to this number of t-channel propagators, a multiperipheral graph will be taken into account. -->
</exchange_lines>
<show_deleted_channels type="T/F" value="F">
<!-- With extra_off_shell_lines, extra channels will be generated which are deleted if they do not contain enough resonances. With this flag, they are just commented out, so they could be manually activated. -->
</show_deleted_channels>
<single_off_shell_decays type="T/F" value="T">
<!-- Whether single-off-shell decays are relevant for the phase space configuration. -->
</single_off_shell_decays>
<double_off_shell_decays type="T/F" value="F">
<!-- Whether double-off-shell decays are relevant for the phase space configuration. -->
</double_off_shell_decays>
<single_off_shell_branchings type="T/F" value="T">
<!-- Whether single-off-shell branchings are relevant for the phase space configuration. -->
</single_off_shell_branchings>
<double_off_shell_branchings type="T/F" value="T">
<!-- Whether double-off-shell branchings are relevant for the phase space configuration. -->
</double_off_shell_branchings>
<massive_fsr type="T/F" value="T">
<!-- Whether the radiation of a massive particle in the final state is relevant for the phase space configuration. -->
</massive_fsr>
<threshold_mass type="float" value="-10">
<!-- A particle with a mass up to this value will be considered as massless for the purpose of phase-space setup. (But the true mass is taken into account when the particle appears as a resonant intermediate state.) -->
</threshold_mass>
<threshold_mass_t type="float" value="-10">
<!-- A particle with a mass up to this value will be considered as massless for the purpose of phase-space setup, when it appears as a t-channel propagator. -->
</threshold_mass_t>
<!-- <initial_decays_fatal type="T/F" value="T"> -->
<!-- As the phase space maps cannot describe on-shell decays of beam particles properly, WHIZARD normally gives a fatal error when such configurations are encountered. This option changes this to a warning at the price of a potentially screwed phase space setup. -->
<!-- </initial_decays_fatal> -->
<default_jet_cut type="float" value="10">
<!-- The default invariant mass cut in GeV applied to pairs of massless colored particles. -->
</default_jet_cut>
<default_mass_cut type="float" value="4">
<!-- The default invariant mass cut in GeV applied to pair production of massless colorless charged particles and to photon emission. -->
</default_mass_cut>
<default_energy_cut type="float" value="10">
<!-- The default energy cut in GeV applied to photon and gluon emission. -->
</default_energy_cut>
<default_q_cut type="float" value="4">
<!-- The default Q cut in GeV applied to photon and gluon exchange. -->
</default_q_cut>
<write_default_cuts_file type="string" value="">
<!-- If nonempty, write the list of default cuts to this file (augmented by the file extension) instead of the default. Note that the settings in this file are overwritten by a user-defined cut configuration, if present. -->
</write_default_cuts_file>
<read_cuts_file type="string" value="">
<!-- Look for user-defined cut configurations in string.cut1 instead of whizard.cut1. -->
</read_cuts_file>
<user_cut_mode type="integer" value="0">
<!-- Set this nonzero to activate a user-defined cut function (Sec. 5.4). -->
</user_cut_mode>
<user_weight_mode type="integer" value="0">
<!-- Set this nonzero to activate a user-defined weight function (Sec. 5.5). -->
</user_weight_mode>
</integration_input>
<simulation_input>
<n_events type="integer" value="0">
<!-- Number of (unweighted) events to generate at least, irrespective of the luminosity setting. -->
</n_events>
<n_calls type="integer" value="0">
<!-- Number of matrix-element calls (weighted events) to execute at least, irrespective of the luminosity setting. -->
</n_calls>
<n_events_warmup type="integer" value="0">
<!-- Number of extra warmup events (see below, Sec. 4.7). -->
</n_events_warmup>
<unweighted type="T/F" value="T">
<!-- Reweight events to generate an unweighted event sample. -->
</unweighted>
<normalize_weight type="T/F" value="T">
<!-- If true, normalize the event weight to unity. If false, normalize to the total cross section. -->
</normalize_weight>
<write_weights type="T/F" value="F">
<!-- If unweighted=F, write weight distribution data to whizard.wgt. -->
</write_weights>
<write_weights_file type="string" value="">
<!-- Write weight distribution to string.wgt instead. -->
</write_weights_file>
<safety_factor type="float" value="1">
<!-- Multiply the estimate for the highest weight by this factor before starting event generation. -->
</safety_factor>
<write_events type="T/F" value="T">
<!-- Write generated events to file whizard.evt to be used by an external analysis package. -->
</write_events>
<write_events_format type="integer" value="20">
<!-- The format to be used for writing events, where the file extension depends on the format (.evt for format = 1, see Sec. 4.7). -->
</write_events_format>
<write_events_file type="string" value="">
<!-- If nonempty, use string as filename for writing events, where the file extension will be appended. -->
</write_events_file>
<events_per_file type="integer" value="5000000">
<!-- If positive, begin a new event file once the number of entries exceeds this number. The event file counter is appended to each event file name, separated with a dot (before the file extension). This feature applies only to non-binary event formats. -->
</events_per_file>
<bytes_per_file type="integer" value="0">
<!-- If positive, begin a new event file once the number of bytes in the file exceeds this number. The event file counter is appended to each event file name, separated with a dot (before the file extension). This feature applies only to non-binary event formats. See Sec. 4.7.1. -->
</bytes_per_file>
<min_file_count type="integer" value="1">
<!-- If event files are split, use this index for the first event file. Increase the counter by one for each successive event file. -->
</min_file_count>
<max_file_count type="integer" value="999">
<!-- Limit for the event file counter; if this limit is exceeded, event generation is terminated. (For weighted events only, this is an error condition since the event sample must be complete for being usable.) -->
</max_file_count>
<write_events_raw type="T/F" value="F">
<!-- Write events to whizard.evx in condensed binary format, so they can be internally reused in another run. -->
</write_events_raw>
<write_events_raw_file type="string" value="">
<!-- Write raw events to string.evx instead. -->
</write_events_raw_file>
<read_events type="T/F" value="F">
<!-- Read events from file whizard.evx (raw format) instead of generating them. This is equivalent to read_events_raw. -->
</read_events>
<read_events_force type="T/F" value="T">
<!-- This was intended to force WHIZARD to read in events from file even if some parameters have changed. However, the MD5 checksum implemented to check for parameter changes has some deficiencies. Hence, we always enforce to read in events, because this feature could otherwise not be used at all. Use with great care! (Note that this problem has been solved in WHIZARD 2.) -->
</read_events_force>
<read_events_raw_file type="string" value="">
<!-- Read raw events from string.evx instead. -->
</read_events_raw_file>
<keep_beam_remnants type="T/F" value="T">
<!-- Keep the beam remnants in the event record when applying structure functions. See Sec. 4.4.8. -->
</keep_beam_remnants>
<keep_initials type="T/F" value="T">
<!-- Keep the beam particles and the partons which initiate the hard scattering in the event record. See Sec. 4.4.8. -->
</keep_initials>
<guess_color_flow type="T/F" value="F">
<!-- Infer the color flow for hadronization from the particle ordering, if it is nontrivial and not available directly. -->
</guess_color_flow>
<recalculate type="T/F" value="F">
<!-- Recalculate the matrix element value for each event of a previously generated sample. Setting this flag automatically turns on reading grids and events from file. -->
</recalculate>
<fragment type="T/F" value="T">
<!-- Fragment the events depending on the value of fragmentation_method (see Sec. 4.8). -->
</fragment>
<fragmentation_method type="integer" value="3">
<!-- Method used for fragmentation if fragment is true: 0=no fragmentation; 1=JETSET; 2=PYTHIA; 3=user. -->
</fragmentation_method>
<user_fragmentation_mode type="integer" value="0">
<!-- When user-defined fragmentation routines are called, this parameter may select different modes. -->
</user_fragmentation_mode>
<pythia_parameters type="string" value="PMAS(25,1)=120.; PMAS(25,2)=0.3605E-02; MSTU(22)=20 ;MSTJ(28)=2 ;PARJ(21)=0.40000;PARJ(41)=0.11000; PARJ(42)=0.52000; PARJ(81)=0.25000; PARJ(82)=1.90000; MSTJ(11)=3; PARJ(54)=-0.03100; PARJ(55)=-0.00200;PARJ(1)=0.08500; PARJ(3)=0.45000; PARJ(4)=0.02500; PARJ(2)=0.31000; PARJ(11)=0.60000; PARJ(12)=0.40000; PARJ(13)=0.72000;PARJ(14)=0.43000; PARJ(15)=0.08000; PARJ(16)=0.08000; PARJ(17)=0.17000; MSTP(3)=1;">
<!-- String to be given to PYTHIA's pygive call before starting event generation. This allows to modify PYTHIA/JETSET properties, set particle masses, etc. The string is also available within user-defined fragmentation routines and can there be abused for different purposes. -->
</pythia_parameters>
<pythia_processes type="string" value="">
<!-- PYTHIA background processes to be simulated in addition to the WHIZARD processes: A list of integers separated by blanks, enclosed in quotation marks. Refer to the PYTHIA manual for the list of processes. -->
</pythia_processes>
<shower type="T/F" value="F">
<!-- Switches the internal shower on or off. As a default it is off. Note that the shower only works with LHEF event format (foramt type 6). This shower is highly experimental. Mainly intended for testing purposes. -->
</shower>
<shower_nf type="integer" value="5">
<!-- Number of light flavors in the shower. -->
</shower_nf>
<shower_running_alpha_s type="T/F" value="F">
<!-- Whether to use a running strong coupling alpha_s or not in the shower. As a default it is fixed. -->
</shower_running_alpha_s>
<shower_alpha_s type="float" value="0.2">
<!-- The value of the strong coupling constant alpha_s as used by the internal shower. The default is 0.2. -->
</shower_alpha_s>
<shower_lambda type="float" value="0.29">
<!-- The value of the QCD scale Lambda_QCD as used by the internal shower. The default is 0.29 GeV. -->
</shower_lambda>
<shower_t_min type="float" value="1.0">
<!-- The infrared cutoff for the evolution parameter tmin as used by the internal shower. The default is 1 GeV. -->
</shower_t_min>
<shower_md type="float" value="0.330">
<!-- The constituent d quark mass md as used by the internal shower. The default is 0.330 GeV. -->
</shower_md>
<shower_mu type="float" value="0.330">
<!-- The constituent u quark mass mu as used by the internal shower. The default is 0.330 GeV. -->
</shower_mu>
<shower_ms type="float" value="0.500">
<!-- The constituent s quark mass ms as used by the internal shower. The default is 0.5 GeV. -->
</shower_ms>
<shower_mc type="float" value="1.5">
<!-- The constituent c quark mass mc as used by the internal shower. The default is 1.5 GeV. -->
</shower_mc>
<shower_mb type="float" value="4.8">
<!-- The constituent b quark mass mb as used by the internal shower. The default is 4.8 GeV.diagnostics_input -->
</shower_mb>
</simulation_input>
<diagnostics_input>
<chattiness type="integer" value="4">
<!-- How much information to show on screen: (0) only fatal errors, (1) and non-fatal errors, (2) and warnings, (3) and messages, (4) and results, (5) and debugging messages (if any). -->
</chattiness>
<catch_signals type="T/F" value="T">
<!-- If the compiler supports it, try to catch external signals such as SIGINT and SIGXCPU and exit gracefully, closing files first. -->
</catch_signals>
<time_limit type="integer" value="0"> -->
<!-- If nonzero, exit gracefully after the given number of minutes has passed. This is useful to prevent an external kill within a batch environment. -->
</time_limit>
<warn_empty_channel type="T/F" value="F">
<!-- Issue a warning whenever the integral within a phase space channel is zero. -->
</warn_empty_channel>
<screen_events type="T/F" value="F">
<!-- Whether to show generated events on screen. -->
</screen_events>
<screen_histograms type="T/F" value="F">
<!-- Whether to show histograms on screen. -->
</screen_histograms>
<screen_diagnostics type="T/F" value="F">
<!-- Whether to repeat the input parameters on screen. -->
</screen_diagnostics>
<show_pythia_banner type="T/F" value="T">
<!-- Whether to display the PYTHIA banner page if fragmentation is enabled. -->
</show_pythia_banner>
<show_pythia_initialization type="T/F" value="T">
<!-- Whether to display the PYTHIA initialization messages if fragmentation is enabled. -->
</show_pythia_initialization>
<show_pythia_statistics type="T/F" value="T">
<!-- Whether to display the PYTHIA statistics summary after event generation is completed. -->
</show_pythia_statistics>
<write_logfile type="T/F" value="T">
<!-- Whether to write the (process-specific) output file(s) whizard.XXX.out. -->
</write_logfile>
<write_logfile_file type="string" value="">
<!-- Use this as the filename for the logfile. -->
</write_logfile_file>
<show_input type="T/F" value="T">
<!-- Whether to repeat the input parameters in the logfile. -->
</show_input>
<show_results type="T/F" value="T">
<!-- Whether to show the integration results in namelist format in the logfile. -->
</show_results>
<show_phase_space type="T/F" value="F">
<!-- Whether to show the phase space configuration in the logfile. -->
</show_phase_space>
<show_cuts type="T/F" value="T">
<!-- Whether to show the cut configuration in the logfile. -->
</show_cuts>
<show_histories type="T/F" value="F">
<!-- Whether to show the individual VAMP channel histories in the logfile. -->
</show_histories>
<show_history type="T/F" value="T">
<!-- Whether to show the overall VAMP history in the logfile. -->
</show_history>
<show_weights type="T/F" value="T">
<!-- Whether to show the weight adaptation in the logfile. -->
</show_weights>
<show_event type="T/F" value="F">
<!-- Whether to show the last event in the logfile. -->
</show_event>
<show_histograms type="T/F" value="F">
<!-- Whether to show histograms in the logfile. -->
</show_histograms>
<show_overflow type="T/F" value="F">
<!-- Whether to show events beyond the first or last bin in histogram listings. -->
</show_overflow>
<show_excess type="T/F" value="T">
<!-- Whether to show a summary of events with weight exceeding one. -->
</show_excess>
<read_analysis_file type="string" value="">
<!-- Use this (string.cut5) as the filename for the analysis setup instead of whizard.cut5 -->
</read_analysis_file>
<plot_width type="float" value="130">
<!-- The width in mm of the plots if online analysis is enabled. -->
</plot_width>
<plot_height type="float" value="90">
<!-- The height in mm of the plots if online analysis is enabled. -->
</plot_height>
<plot_excess type="T/F" value="T">
<!-- In the plots, display excess events in red. -->
</plot_excess>
<plot_history type="T/F" value="T">
<!-- If this is enabled, write a graphics driver file for displaying the integration history, i.e., the integral with error bars for each iteration. Use make history to generate the graphics file whizard-history.ps. -->
</plot_history>
<plot_grids_channels type="string" value="">
<!-- The string is a list of phase-space channels (integers) for which the bin distribution will be histogrammed. Use make grids to generate the graphics file whizard-grids.ps. -->
</plot_grids_channels>
<plot_grids_logscale type="float" value="10">
<!-- Use logarithmic scale for the grid plots if the bin width varies over more than this ratio. -->
</plot_grids_logscale>
<slha_rewrite_input type="T/F" value="T">
<!-- If SUSY Les Houches Accord data have been used, whether to repeat this input in the process-specific logfiles (including comments) or to rewrite it there using the data which have actually been used. -->
</slha_rewrite_input>
<slha_ignore_errors type="T/F" value="F">
<!-- If this is false, an error signaled in the SLHA input file (in the SPINFO or DCINFO block) will cause WHIZARD to stop before calculating anything. If true, such errors will be displayed, but the run continues. -->
</slha_ignore_errors>
</diagnostics_input>
%s
<beam_input_1>
<energy type="float" value="0">
<!-- If greater than the beam particle mass, this specifies the beam energy in the lab frame. Otherwise, the beam energy is set equal to the particle mass (fixed target). -->
</energy>
<angle type="float" value="0">
<!-- If direction is not set, this specifies a rotation of the beam axis in the lab frame around the positive y axis. (By default, the beam directions are along the positive/negative z axis, so a rotation by the angle pi/2 turns them into the positive/negative x axis.) If direction is set, this parameter is ignored. -->
</angle>
<direction type="floatarray" value="0 0 0">
<!-- If any component is nonzero, this vector explicitly specifies the direction of the given beam in the lab frame. -->
</direction>
<vector_polarization type="T/F" value="F">
<!-- If false (default), use the standard helicity basis (left-/right-handed). Set this flag if you need another basis, in particular transversal polarization. -->
</vector_polarization>
<polarization type="floatarray" value="0.0 0.0">
<!-- Fraction of left/right polarization (fermions, photons, gluons), resp. left/longitudinal/right polarization (massive vector bosons). If the vector polarization model is selected, the three numbers denote the polarization vector. -->
</polarization>
<particle_code type="integer" value="0">
<!-- PDG code of the incoming beam particle. -->
</particle_code>
<particle_name type="string" value="e1">
<!-- Name of the incoming beam particle. -->
</particle_name>
<USER_spectrum_on type="T/F" value="T">
<!-- Apply or not the user spectrum -->
</USER_spectrum_on>
<USER_spectrum_mode type="integer" value="11">
<!-- User spectrum -->
</USER_spectrum_mode>
<ISR_on type="T/F" value="T">
<!-- Whether to apply ISR (electron or positron beam). -->
</ISR_on>
<ISR_alpha type="float" value="0.0072993">
<!-- The value of alpha_QED to be used for the spectrum. -->
</ISR_alpha>
<ISR_m_in type="float" value="0.000511">
<!-- The mass of the incoming particle. -->
</ISR_m_in>
<ISR_Q_max type="float" value="sqrts">
<!-- The hard scale which cuts off photon radiation. -->
</ISR_Q_max>
<ISR_LLA_order type="0/1/2/3" value="3">
<!-- The order of the leading-logarithmic approximation. -->
</ISR_LLA_order>
<ISR_map type="T/F" value="T">
<!-- Whether to use a mapping of the singularity at x=1 when evaluating the structure function (recommended; note that switching this off might even lead to an uncaught arithmetic exception). -->
</ISR_map>
<EPA_on type="T/F" value="F">
<!-- Whether to use the EPA spectrum (photon beam). -->
</EPA_on>
<EPA_map type="T/F" value="T">
<!-- Whether to apply a mapping to improve convergence. -->
</EPA_map>
<EPA_alpha type="float" value="0.0072993">
<!-- The value of alpha_QED to be used for the spectrum. -->
</EPA_alpha>
<EPA_m_in type="float" value="0.000511">
<!-- The mass of the incoming beam particle. -->
</EPA_m_in>
<EPA_mX type="float" value="4">
<!-- The lower cutoff for the produced invariant mass. -->
</EPA_mX>
<EPA_Q_max type="float" value="4">
<!-- The upper cutoff on the virtuality of the photon (Qmax&gt;0). -->
</EPA_Q_max>
<EPA_x0 type="float" value="0">
<!-- The lower cutoff on the energy fraction of the incoming photon -->
</EPA_x0>
<EPA_x1 type="float" value="0">
<!-- The upper cutoff on the energy fraction of the incoming photon -->
</EPA_x1>
</beam_input_1>
<beam_input_2>
<energy type="float" value="0">
<!-- If greater than the beam particle mass, this specifies the beam energy in the lab frame. Otherwise, the beam energy is set equal to the particle mass (fixed target). -->
</energy>
<angle type="float" value="0">
<!-- If direction is not set, this specifies a rotation of the beam axis in the lab frame around the positive y axis. (By default, the beam directions are along the positive/negative z axis, so a rotation by the angle pi/2 turns them into the positive/negative x axis.) If direction is set, this parameter is ignored. -->
</angle>
<direction type="floatarray" value="0 0 0">
<!-- If any component is nonzero, this vector explicitly specifies the direction of the given beam in the lab frame. -->
</direction>
<vector_polarization type="T/F" value="F">
<!-- If false (default), use the standard helicity basis (left-/right-handed). Set this flag if you need another basis, in particular transversal polarization. -->
</vector_polarization>
<polarization type="floatarray" value="0.0 0.0">
<!-- Fraction of left/right polarization (fermions, photons, gluons), resp. left/longitudinal/right polarization (massive vector bosons). If the vector polarization model is selected, the three numbers denote the polarization vector. -->
</polarization>
<particle_code type="integer" value="0">
<!-- PDG code of the incoming beam particle. -->
</particle_code>
<particle_name type="string" value="E1">
<!-- Name of the incoming beam particle. -->
</particle_name>
<USER_spectrum_on type="T/F" value="T">
<!-- Apply or not the user spectrum -->
</USER_spectrum_on>
<USER_spectrum_mode type="integer" value="-11">
<!-- User spectrum -->
</USER_spectrum_mode>
<ISR_on type="T/F" value="T">
<!-- Whether to apply ISR (electron or positron beam). -->
</ISR_on>
<ISR_alpha type="float" value="0.0072993">
<!-- The value of alpha_QED to be used for the spectrum. -->
</ISR_alpha>
<ISR_m_in type="float" value="0.000511">
<!-- The mass of the incoming particle. -->
</ISR_m_in>
<ISR_Q_max type="float" value="sqrts">
<!-- The hard scale which cuts off photon radiation. -->
</ISR_Q_max>
<ISR_LLA_order type="0/1/2/3" value="3">
<!-- The order of the leading-logarithmic approximation. -->
</ISR_LLA_order>
<ISR_map type="T/F" value="T">
<!-- Whether to use a mapping of the singularity at x=1 when evaluating the structure function (recommended; note that switching this off might even lead to an uncaught arithmetic exception). -->
</ISR_map>
<EPA_on type="T/F" value="F">
<!-- Whether to use the EPA spectrum (photon beam). -->
</EPA_on>
<EPA_map type="T/F" value="T">
<!-- Whether to apply a mapping to improve convergence. -->
</EPA_map>
<EPA_alpha type="float" value="0.0072993">
<!-- The value of alpha_QED to be used for the spectrum. -->
</EPA_alpha>
<EPA_m_in type="float" value="0.000511">
<!-- The mass of the incoming beam particle. -->
</EPA_m_in>
<EPA_mX type="float" value="4">
<!-- The lower cutoff for the produced invariant mass. -->
</EPA_mX>
<EPA_Q_max type="float" value="4">
<!-- The upper cutoff on the virtuality of the photon (Qmax&gt;0). -->
</EPA_Q_max>
<EPA_x0 type="float" value="0">
<!-- The lower cutoff on the energy fraction of the incoming photon -->
</EPA_x0>
<EPA_x1 type="float" value="0">
<!-- The upper cutoff on the energy fraction of the incoming photon -->
</EPA_x1>
</beam_input_2>
</whizard>
"""%modelparams)
    self.getInputFiles(model)
  
  def getInputFiles(self, model):
    """ Get the proper input parameter file, usually LesHouches
    """
    if not self.paramdict.has_key('process_input'):
      self.paramdict['process_input'] = {}
    if not self.paramdict['process_input'].has_key('input_file'):
      res = self.genmodel.getFile(model) 
      if not res['OK']:
        self.paramdict['process_input']['input_file'] = ''
        self.paramdict['process_input']['input_slha_format'] = 'F'
      else:
        self.paramdict['process_input']['input_file'] = res['Value']
        self.paramdict['process_input']['input_slha_format'] = 'T'
    
    
  def modelParams(self, model):
    """ Get the model parameters
    """
    modelparams = []
    res = self.genmodel.getParamsForWhizard(model)
    if not res['OK']:
      return ""
    modelparams.append("<parameter_input>")

    modelparams.append(res['Value'])
    
    modelparams.append("</parameter_input>")
    
    return "\n".join(modelparams)
    
  def toXML(self, fname = 'whizard.xml'):
    """ Write to XML
    """
    tree = ElementTree(self.whizardxml)
    tree.write(fname)
    return S_OK()
  
  def getMainFields(self):
    """ Get the main fields
    """
    listoffields = []
    for elem in self.whizardxml.getchildren():
      listoffields.append(elem.tag)
    return S_OK(listoffields)
  
  def getOptionsForField(self, field):
    """ Get the options of a given field
    """
    options = []
    element = self.whizardxml.find(field)
    if element == None:
      return S_ERROR("Field %s does not exist" % field)
    for subelements in element.getchildren():
      options.append(subelements.tag)
    return S_OK(options)
  
  def getValue(self, field):
    """ Get the value for a given field/option
    """
    element = self.whizardxml.find(field)
    return S_OK(element.attrib['value'])  

  def changeAndReturn(self, paramdict):
    """ Update the options, and returns the modified XML object
    """
    self.paramdict.update(paramdict)
    res = self.checkFields(self.paramdict)
    if not res['OK']:
      return res
    for key, val in self.paramdict.items():
      for subkey in val.keys():
        subelement = self.whizardxml.find(key + "/" + subkey)
        subelement.attrib['value'] = val[subkey]
    return S_OK(self.whizardxml)
  
  def getAsDict(self):
    """ Get the content as dict, like the one used for setting the options
    """
    whiz_opt = {}
    for element in self.whizardxml.getchildren():
      whiz_opt[element.tag] = {}
      for item in element.getchildren():
        val = item.attrib['value']
        if type(val) == type(""):
          val = val.rstrip()
        whiz_opt[element.tag][item.tag] = val
    return S_OK(whiz_opt)
  
  def checkFields(self, paramdict):
    """ Make sure all supplied fields are exisiting somewhere
    """
    for key, val in paramdict.items():
      element = self.whizardxml.find(key)
      if element == None:
        return S_ERROR("Element %s is not in the allowed parameters" % key)
      for subkey, value in val.items():
        subelement = self.whizardxml.find(key + "/" + subkey)
        if subelement == None:
          return S_ERROR("Key %s/%s is not in the allowed parameters" % (key, subkey))
        etype = subelement.attrib['type']
        if etype == 'float':
          if not type(value) == types.FloatType and not type(value) == types.IntType:
            return S_ERROR("%s should be a float" % (key + "/" + subkey))
        elif etype == 'T/F':
          if value != 'T' and value != 'F':
            return S_ERROR("%s should be either 'T' or 'F'" % (key + "/" + subkey))
        elif etype == 'integer' or type == '0/1/2/3':
          if not type(value) == types.IntType:
            return S_ERROR("%s should be an integer" % (key + "/" + subkey))
        elif etype == 'string':
          if not type(value) in types.StringTypes:
            return S_ERROR("%s should be a string" % (key + "/" + subkey))
        elif etype == 'floatarray':
          error = False
          if not type(value) in types.StringTypes:
            error = True
          else:
            valelem = value.split()
            if len(valelem) < 2:
              error = True
          if error: 
            return S_ERROR("%s should be a string with spaces, e.g. '0 1 2 3'" % (key + "/" + subkey))
    return S_OK()
  
  def toWhizardDotIn(self, fname):
    """ Write the options to the whizard.in
    """
    lines = []
    for elem in self.whizardxml.getchildren():
      tag = elem.tag
      if tag.count("beam_input"):
        tag = "beam_input"
      lines.append("&%s" % tag)
      for subelem in elem.getchildren():
        val = subelem.get('value')
        if val == 'sqrts':
          continue
        if subelem.get('type') == 'string' :
          val = '"%s"' % val
        if val == '000':
          val = '0 0 0'
        if val == '0.0.0':
          val = '0.0 0.0'
        if val == '0..0..0':
          val = '\n 1 20000\n 10 20000\n 1 20000'
        lines.append(' %s = %s' % (subelem.tag, val))
      lines.append('/')
    of = file(fname, "w")
    of.write("\n".join(lines))
    of.write("\n")
    return S_OK(True)
  
