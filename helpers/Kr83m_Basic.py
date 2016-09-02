import hax

class Kr83m_Basic(hax.minitrees.TreeMaker):
    
    __version__ = '0.1.0'
    extra_branches = ['peaks.n_contributing_channels',
                      'peaks.hit_time_mean',
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
        
        # assume one kr signal (32 or 9 keV) is interactions[0]
        s1a = interactions[0].s1
        s2a = interactions[0].s2
        
        # find another kr interaction
        krInt = [0,0]  
        for i, interaction in enumerate(interactions):
            if interaction.s1 != s1a and interaction.s2 == s2a and krInt[0] == 0:
                krInt[0] = i
            elif interaction.s1 != s1a and interaction.s2 != s2a and krInt[1] == 0:
                krInt[1] = i
    
        # Distinction b/w single and double s2 events
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
    
        event_data.update(dict( s10Area = peaks[s10].area,
                                cs10Area = peaks[s10].area*interactions[i0].s1_area_correction,
                                s10Coin = peaks[s10].n_contributing_channels,
                                s10Time = peaks[s10].hit_time_mean,
                                i0x = interactions[i0].x,
                                i0y = interactions[i0].y,
                                i0z = interactions[i0].z,
                                i0DriftTime = interactions[i0].drift_time,
                                s20Area = peaks[s20].area,
                                cs20Area = peaks[s20].area*interactions[i0].s2_area_correction,
                                s20Coin = peaks[s20].n_contributing_channels,
                                s20Time = peaks[s20].hit_time_mean,
                                s11Area = peaks[s11].area,
                                cs11Area = peaks[s11].area*interactions[i1].s1_area_correction,
                                s11Coin = peaks[s11].n_contributing_channels,
                                s11Time = peaks[s11].hit_time_mean,
                                i1x = interactions[sInt].x,
                                i1y = interactions[sInt].y,
                                i1z = interactions[sInt].z,
                                i1DriftTime = interactions[i1].drift_time,
                                s21Area = peaks[s21].area,
                                cs20Area = peaks[s21].area*interactions[i1].s2_area_correction,
                                s21Coin = peaks[s21].n_contributing_channels,
                                s21Time = peaks[s21].hit_time_mean,
                                secondS2 = secondS2 ))
              
        return event_data        
