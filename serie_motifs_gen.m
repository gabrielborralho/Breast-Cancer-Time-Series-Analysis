clear all; close all; clc;

n=0;
Tjanela=13; %TAMANHO DA JANELA
janela=Tjanela;
qtdPacientes = 35; %quantidade de pacientes
discord_1st=zeros(20);

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
            motif_1st(i,1)=matrixProfile(motifIdxs{1}(1)+(i-1)); % ver {1}(1) em https://la.mathworks.com/videos/cell-arrays-for-holding-different-data-types-97321.html
        end
        
        motifLen = length(motif_1st);
        fid = fopen(strcat('C:\Users\Gabriel Borralho\Documents\MEGA\LabPAI\MATRIX_PROFILE\Mseries',num2str(janela),'x',num2str(janela),'\M_',TipoPacientes,'_ID_',num2str(Endereco),'.txt'),'wt');
        for i=1:1:motifLen
            fprintf(fid,'%f\n',motif_1st(i,1));
        end
        fclose(fid);
               
        %índice para acompanhar processo no Command Window
        n=n+1;%contador
        disp(strcat('Série de Motifs de ID_', Endereco, ' n=', num2str(n)))        
        clear ST;
    end    
    TipoPacientes='saudaveis';
end
disp('Séries Motifs Matrix Profile Salvas!')