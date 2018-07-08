clear all; close all; clc;

n=0;
Tjanela=13; %TAMANHO DA JANELA
janela=Tjanela;
qtdPacientes = 35; %quantidade de pacientes

TipoPacientes='doentes';
for a=1:1:2 %Loop para Classe (Doentes ou Saudaveis)
    enderecos=importdata(strcat('C:\Users\Gabriel Borralho\Documents\MEGA\LabPAI\Data_of_patients\',TipoPacientes,'\Enderecos_',TipoPacientes,'.txt'));
    disp(strcat('Importou endereços de:',' C:\Users\Gabriel Borralho\Documents\MEGA\LabPAI\Data_of_patients\',TipoPacientes,'\Enderecos_',TipoPacientes,'.txt'))

    for p=1:1:qtdPacientes %Loop para pacientes
        Endereco=num2str(enderecos(p,1));
        
        ST=importdata(strcat('C:\Users\Gabriel Borralho\Documents\MEGA\LabPAI\MATRIX_PROFILE\series',num2str(janela),'\ST_',TipoPacientes,'_ID_',num2str(Endereco),'.txt'));

        subLen=20;
        ST=ST(:);        

        [matrixProfile, profileIndex, motifIdxs, discordIdx] = interactiveMatrixProfileVer2(ST,subLen);

        MPLen = length(matrixProfile);
        fid = fopen(strcat('C:\Users\Gabriel Borralho\Documents\MEGA\LabPAI\MATRIX_PROFILE\MPseries',num2str(janela),'x',num2str(janela),'\MP_',TipoPacientes,'_ID_',num2str(Endereco),'.txt'),'wt');
        for i=1:1:MPLen
            fprintf(fid,'%f\n', matrixProfile(i,1));
        end
        fclose(fid);
        
        save(strcat('C:\Users\Gabriel Borralho\Documents\MEGA\LabPAI\MATRIX_PROFILE\motif',num2str(janela),'x',num2str(janela),'\',TipoPacientes,'\motif_',TipoPacientes,'_ID_', num2str(Endereco)),'motifIdxs');
        save(strcat('C:\Users\Gabriel Borralho\Documents\MEGA\LabPAI\MATRIX_PROFILE\discord',num2str(janela),'x',num2str(janela),'\',TipoPacientes,'\discord_',TipoPacientes,'_ID_', num2str(Endereco)),'discordIdx');
        
        
        %índice para acompanhar processo no Command Window
        n=n+1;%contador
        disp(strcat('Matrix Profile de ID_', Endereco, ' n=', num2str(n)))
        
        clear ST;
    end    
    TipoPacientes='saudaveis';
end

disp('Séries Matrix Profile Salvas!')


