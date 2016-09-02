import hax

class DoubleScatter(hax.minitrees.TreeMaker):
    
    __version__ = '0.0.1'
    extra_branches = ['peaks.n_contributing_channels',
                      'peaks.hit_time_mean',
                      'peaks.center_time',
                      'peaks.area_fraction_top']
    
    def extract_data(self, event):
        
        # If there are no interactions at all, we can't extract anything...
        if not len(event.interactions):
            return dict()
        
        event_data = dict(event_number=event.event_number,
                          event_time=event.start_time)
        
        # shortcuts for pax classes
        peaks = event.peaks
        interactions = event.interactions
        
        # assume one scatter is interactions[0]
        s1a = interactions[0].s1
        s2a = interactions[0].s2
        
        # find another scatter
        krInt = [0,0]  
        for i, interaction in enumerate(interactions):
            if interaction.s1 != s1a and interaction.s2 == s2a and krInt[0] == 0:
                krInt[0] = i
            elif interaction.s1 != s1a and interaction.s2 != s2a and krInt[1] == 0:
                krInt[1] = i
    
        # Distinction b/w single and double s2 scatters
        # Cut events without second s1
        if krInt[1] != 0:
            s1b = interactions[krInt[1]].s1
            s2b = interactions[krInt[1]].s2
            sInt = krInt[1]
            secondS2 = 1
        elif krInt[0] != 0:
            s1b = interactions[krInt[0]].s1
            s2b = interactions[0].s2
            sInt = krInt[0]
            secondS2 = 0
        else: return dict()
                                
        # order s1s/interactions by time
        if peaks[s1a].hit_time_mean <= peaks[s1b].hit_time_mean:
            s10 = s1a
            s11 = s1b
            s20 = s2a
            s21 = s2b
            i0 = 0
            i1 = sInt
        else:
            s10 = s1b
            s11 = s1a
            s20 = s2b
            s21 = s2a
            i0 = sInt
            i1 = 0
                
        ##### Grab Data #####
    
        event_data.update(dict( s1_0 = peaks[s10].area,
                                cs1_0 = peaks[s10].area*interactions[i0].s1_area_correction,
                                s1_0_area_fraction_top = peaks[s10].area_fraction_top,
                                s1_0_n_contributing_channels = peaks[s10].n_contributing_channels,
                                s1_0_hit_time_mean = peaks[s10].hit_time_mean,
                                s1_0_center_time = peaks[s10].center_time,
                                
                                s2_0 = peaks[s20].area,
                                cs2_0 = peaks[s20].area*interactions[i0].s2_area_correction,
                                s2_0_area_fraction_top = peaks[s20].area_fraction_top,
                                s2_0_n_contributing_channels = peaks[s20].n_contributing_channels,
                                s2_0_hit_time_mean = peaks[s20].hit_time_mean,
                                s2_0_center_time = peaks[s20].center_time,
                               
                                int_0_x = interactions[i0].x,
                                int_0_y = interactions[i0].y,
                                int_0_z = interactions[i0].z,
                                int_0_drift_time = interactions[i0].drift_time,
                               
                                s1_1 = peaks[s11].area,
                                cs1_1 = peaks[s11].area*interactions[i1].s1_area_correction,
                                s1_1_area_fraction_top = peaks[s11].area_fraction_top,
                                s1_1_n_contributing_channels = peaks[s11].n_contributing_channels,
                                s1_1_hit_time_mean = peaks[s11].hit_time_mean,
                                s1_1_center_time = peaks[s11].center_time,
                                                               
                                s2_1 = peaks[s21].area,
                                cs2_1 = peaks[s21].area*interactions[i1].s2_area_correction,
                                s2_1_area_fraction_top = peaks[s21].area_fraction_top,
                                s2_1_n_contributing_channels = peaks[s21].n_contributing_channels,
                                s2_1_hit_time_mean = peaks[s21].hit_time_mean,
                                s2_1_center_time = peaks[s21].center_time,
                               
                                int_1_x = interactions[i1].x,
                                int_1_y = interactions[i1].y,
                                int_1_z = interactions[i1].z,
                                int_1_drift_time = interactions[i1].drift_time,
                               
                                secondS2 = secondS2 ))
              
        return event_data        
