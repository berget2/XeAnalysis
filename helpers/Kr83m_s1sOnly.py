import hax

class Kr83m_s1sOnly(hax.minitrees.TreeMaker):

    __version__ = '0.1.0'
    extra_branches = ['peaks.n_contributing_channels',
                      'peaks.hit_time_mean',
                      'peaks.left',
                      'peaks.right',
                      'event.s1s',
                      'peaks.reconstructed_positions']

    def extract_data(self, event):
        
        if len(event.s1s) < 2: 
            return dict()


        event_data = dict(  event_number = event.event_number,
                            event_time = event.start_time )

        # shortcuts for pax classes
        peaks = event.peaks
        
        # select two largest s1s
        s1a = event.s1s[0]
        s1b = event.s1s[1]
        
        # order s1s by time
        if peaks[s1a].hit_time_mean <= peaks[s1b].hit_time_mean:
            s10 = s1a
            s11 = s1b
        else:
            s10 = s1b
            s11 = s1a
            
            
        ##### Grab Data #####
        
        event_data.update(dict( s10Area = peaks[s10].area,
                                s10Coin = peaks[s10].n_contributing_channels,
                                s10Time = peaks[s10].hit_time_mean,
                                s10LeftEdge = peaks[s10].left*10.0,
                                s10RightEdge = peaks[s10].right*10.0,
                                i0x = peaks[s10].reconstructed_positions[0].x, # 'interaction' label retained for consistency
                                i0y = peaks[s10].reconstructed_positions[0].y,
                                s11Area = peaks[s11].area,
                                s11Coin = peaks[s11].n_contributing_channels,
                                s11Time = peaks[s11].hit_time_mean,
                                s11LeftEdge = peaks[s11].left*10.0,
                                s11RightEdge = peaks[s11].right*10.0,
                                i1x = peaks[s11].reconstructed_positions[0].x,
                                i1y = peaks[s11].reconstructed_positions[0].y))

        return event_data