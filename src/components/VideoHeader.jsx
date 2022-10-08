import React from 'react';
import video_mobile from '../assets/media/WEBLOOP_mobile.mp4';
import video_desktop from '../assets/media/WEBLOOP_desktop.mp4';
import Media from 'react-media';

export default function VideoHeader() {
 
  return (
    <div>
      <Media queries={{
        mobile: "(max-width: 479px)",
        desktop: "(min-width: 480px)"
      }}>
        {matches => (
          <div style={{flex: 1}}>
          {matches.mobile && <video
          autoPlay
          loop
          muted
          playsInline
          src={video_mobile}
          width='100%'
          type="video/mp4"
        />}
          {matches.desktop && <video
          autoPlay
          loop
          muted
          playsInline
          src={video_desktop}
          width='100%'
          type="video/mp4"
        />}
          </div>
        )}
      </Media>
      
    </div>
  );
}


