clear all; close all; clc;

%PARA Paciente em Conjunto(Pacientes) FAÇA:
%       serie  <- EXTRAIR_SERIE(Paciente)
%       rotulo <- OBTER_ROTULO (Paciente)
%       [caract1,caract2,caract3, caract4, caract5, rotulo] = EXTRAIR_CARACTERISTICAS(serie,rotulo)
%       ESCREVA_ARQUIVO("caract1,caract2,caract3, caract4, caract5, rotulo")
%FIM

n=0;
Tjanela=13; %TAMANHO DA JANELA
janela=Tjanela;
qtdPacientes = 35; %quantidade de pacientes

fid = fopen(strcat('feat8_',num2str(janela),'x',num2str(janela),'.txt'),'wt') % nome do arquivo das características, antes do laço

TipoPacientes='doentes';
rotulo=1; %Rótulo para doentes
for a=1:1:2
    enderecos=importdata(strcat('C:\Users\Gabriel Borralho\Documents\MEGA\LabPAI\Data_of_patients\',TipoPacientes,'\Enderecos_',TipoPacientes,'.txt'));
    disp(strcat('Importou endereços de:',' C:\Users\Gabriel Borralho\Documents\MEGA\LabPAI\Data_of_patients\',TipoPacientes,'\Enderecos_',TipoPacientes,'.txt'))

    for p=1:1:qtdPacientes %Loop para pacientes
        Endereco=num2str(enderecos(p,1));
        ST=importdata(strcat('C:\Users\Gabriel Borralho\Documents\MEGA\LabPAI\Data_of_patients\series\series',num2str(janela),'x',num2str(janela),'\',TipoPacientes,'\ST_',TipoPacientes,'_ID_', Endereco,'.mat'));
        %disp(strcat('C:\Users\Gabriel Borralho\Documents\MEGA\LabPAI\Data_of_patients\series\series',num2str(janela),'x',num2str(janela),'\',TipoPacientes,'\ST_',TipoPacientes,'_ID_', Endereco,'.mat'))
        [IEMG,MAV,MMAV,SSI,VAR,RMS,V2,V3,LOG,WL,ACC,DASDV,MFL,MYOP,TTP,WAMP] = featuresST(ST);
        
        %gravar
        
        %%LibSVM Todas
        %fprintf(fid,'%d 1:%f 2:%f 3:%f 4:%f 5:%f 6:%f 7:%f 8:%f 9:%f 10:%f 11:%f 12:%f 13:%f 14:%f 15:%f 16:%f\n',rotulo,IEMG,MAV,MMAV,SSI,VAR,RMS,V2,V3,LOG,WL,ACC,DASDV,MFL,MYOP,TTP,WAMP); %LibSVM
        %select features: [13, 8, 6, 7, 2, 3, 9, 12]
        fprintf(fid,'%d 1:%f 2:%f 3:%f 4:%f 5:%f 6:%f 7:%f 8:%f\n',rotulo,MAV,MMAV,RMS,V2,V3,LOG,DASDV,MFL); %LibSVM
        
        %%MATLAB
        %fprintf(fid,'%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%s\n',IEMG,MAV,MMAV,SSI,VAR,RMS,V2,V3,LOG,WL,ACC,DASDV,MFL,MYOP,TTP,WAMP,TipoPacientes); %MATLAB

        
        %índice para acompanhar processo no Command Window
        n=n+1;%contador
        disp(strcat('Caracteristicas de ID_', Endereco, ' n=', num2str(n)))

        %Salva as características .mat
        %save(strcat('C:\Users\Gabriel Borralho\Documents\MEGA\LabPAI\Data_of_patients\features\features',num2str(janela),'x',num2str(janela),'\',TipoPacientes,'\features_',TipoPacientes,'_ID_', Endereco),'IEMG','MAV','MMAV','SSI','VAR','RMS','V2','V3','LOG','WL','ACC','DASDV','MFL',TipoPacientes); %MUDAR AQUI
        clear ST;
    end    
    TipoPacientes='saudaveis';
    rotulo=-1; %Rótulo para saudaveis
end
fclose(fid); %depois do laço
disp('Caracteristicas Salvas!') 