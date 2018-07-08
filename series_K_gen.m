clear all; close all; clc;

n=0;
Tjanela=11; %TAMANHO DA JANELA
janela=Tjanela;
qtdPacientes = 35; %quantidade de pacientes

TipoPacientes='doentes';
for a=1:1:2 %Laço para Classe (Doentes ou Saudaveis)
    enderecos=importdata(strcat('C:\Users\Gabriel Borralho\Documents\MEGA\LabPAI\Data_of_patients\',TipoPacientes,'\Enderecos_',TipoPacientes,'.txt'));
    disp(strcat('Importou endereços de:',' C:\Users\Gabriel Borralho\Documents\MEGA\LabPAI\Data_of_patients\',TipoPacientes,'\Enderecos_',TipoPacientes,'.txt'))

    for p=1:1:qtdPacientes %Loop para pacientes
        Endereco=num2str(enderecos(p,1));
        
        ST=importdata(strcat('C:\Users\Gabriel Borralho\Documents\MEGA\LabPAI\MATRIX_PROFILE\series',num2str(janela),'\ST_',TipoPacientes,'_ID_',num2str(Endereco),'.txt'));
        subLen=20;
        ST=ST(:); %Faz ST ficar unidimensional

        [matrixProfile, profileIndex, motifIdxs, discordIdx] = interactiveMatrixProfileVer2(ST,subLen);
        close %fecha a janela do Matrix Profile
        
        for i=1:1:20 %Extrai Motif e Discord de matrixProfile baseados nos endereços informado por motifIdxs e discordIdx
            discord_1st(i,1)=matrixProfile(discordIdx(1)+(i-1));
            motif_1st(i,1)=matrixProfile(motifIdxs{1}(1)+(i-1)); % ver {1}(1) em https://la.mathworks.com/videos/cell-arrays-for-holding-different-data-types-97321.html
        end
        serieK=vertcat(discord_1st,motif_1st); %concatena motif e discord em serieK
        
        KLen = length(serieK);
        fid = fopen(strcat('C:\Users\Gabriel Borralho\Documents\MEGA\LabPAI\MATRIX_PROFILE\Kseries',num2str(janela),'x',num2str(janela),'\K_',TipoPacientes,'_ID_',num2str(Endereco),'.txt'),'wt');
        for i=1:1:KLen
            fprintf(fid,'%f\n', serieK(i,1));
        end
        fclose(fid);
               
        %índice para acompanhar processo no Command Window
        n=n+1;%contador
        disp(strcat('Série Reduzida K de ID_', Endereco, ' n=', num2str(n)))        
        clear ST;
    end    
    TipoPacientes='saudaveis';
end
disp('Séries Reduzidas Matrix Profile Salvas!')