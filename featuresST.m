function [IEMG,MAV,MMAV,SSI,VAR,RMS,V2,V3,LOG,WL,ACC,DASDV,MFL,MYOP,TTP,WAMP] = featuresST(ST)
    %ST -> Série Temporal
    IEMG=0;MMAV=0;SSI=0;VAR=0;RMS=0;V2=0;V3=0;LOG=0;WL=0;ACC=0;DASDV=0;MFL=0;MYOP=0;WAMP=0;TTP=0;
    transposta=ST';
    ST=transposta(:); %transforma ST em superserie de uma dimensão
    [N,c]=size(ST);
    
    %% 1:IEMG Integrated EMG
    for f=1:1:N
        IEMG=IEMG+abs(ST(f,c));
    end
    %IEMG_MAT=sumabs(ST) %Comparar com a função do MATLAB
    
    %% 2:MAV Mean Absolute Value
    MAV=IEMG/N;
    %MAV_MAT=meanabs(ST) %Comparar com a função do MATLAB

    %% 3:MMAV Modified Mean Absolute Value
    for f=1:1:N
        if((ST(f,c)>= 0.25*N) && (ST(f,c)<= 0.75*N))
            MMAV=MMAV+abs(ST(f,c));
        else
            MMAV=MMAV+0.5*abs(ST(f,c));
        end
    end
    MMAV=MMAV/N;

    %% 4:SSI Simple Square Integral
    for f=1:1:N
        SSI=SSI+(abs(ST(f,c)))^2;
    end
    
    %% 5:VAR Variance
    for f=1:1:N
        VAR=VAR+((ST(f,c)-MAV)^2);
    end
    VAR = VAR/(N-1);
    %VAR_MAT=var(ST) %Comparar com a função do MATLAB

    %% 6:RMS Root Mean Square
    for f=1:1:N
        RMS=RMS+((ST(f,c))^2);
    end
    RMS=sqrt((1/N)*RMS);
    %RMS_MAT=rms(ST) %Comparar com a função do MATLAB

    %% 7: v-Order: V2
    for f=1:1:N
        V2=V2+(ST(f,c)^2);
    end
    V2=((1/N)*V2)^(1/2);
    %% 8: v-Order: V3
    for f=1:1:N
        V3=V3+(abs(ST(f,c))^3);
    end
    V3=((1/N)*V3)^(1/3);

    %% 9:LOG Log Detector
    for f=1:1:N
        LOG=LOG+log((abs(ST(f,c))));
    end
    LOG=exp(((1/N)*LOG));

    %% 10:WL Waveform Lenght
    for f=1:1:N-1
        WL=WL+abs(ST(f+1,c)-ST(f,c));
    end
    %% 11:AAC Average Amplitude Change
    ACC=(1/N)*WL;

    %% 12: DASDV Difference Absolute Standard Deviation Value
    for f=1:1:N-1
        DASDV=DASDV+(ST(f+1,c)-ST(f,c))^2;
    end
    DASDV=sqrt((1/(N-1))*DASDV);

    %% 13: MFL Maximum Fractal Lenght
    for f=1:1:N-1
        MFL=MFL+(ST(f+1,c)-ST(f,c))^2;
    end
    MFL=log10(sqrt(MFL));
    
    %% 14: MYOP Myopulse percentage rate
    threshold=MAV;
    for f=1:1:N
        if(ST(f,c) >= threshold)
            MYOP=MYOP+1;
        end
    end
    MYOP=MYOP/N;
    
    %% 15: TTP Total Power Spectral Density
    pxx = periodogram(ST);
    M = length(pxx);
    for f=1:1:M
        TTP=TTP+(pxx(f,c));
    end
    
    %% 16: WAMP Willison Amplitude
    threshold=MAV;
    for f=1:1:N-1
        if(ST(f,c) >= threshold)
            WAMP=WAMP+ abs(ST(f,c)-ST(f+1,c));
        end
    end
end