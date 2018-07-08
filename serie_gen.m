clear all; close all; clc;
% Gera n séries de tamanho 20 para cada paciente
Tjanela=11;% TAMANHO DA JANELA
linha=1; coluna=1; cond=0; temp_media=0;n=0;
janela=Tjanela;

qtdPacientes = 35; %quantidade de pacientes
num_tempos = 20; %quantidade de imagens por exame

TipoPacientes='doentes';
for a=1:1:2    
    enderecos=importdata(strcat('C:\Users\Gabriel Borralho\Documents\MEGA\LabPAI\Data_of_patients\',TipoPacientes,'\Enderecos_',TipoPacientes,'.txt'));
    disp(strcat('Importou endereços de:',' C:\Users\Gabriel Borralho\Documents\MEGA\LabPAI\Data_of_patients\',TipoPacientes,'\Enderecos_',TipoPacientes,'.txt'))

    for p=1:1:qtdPacientes %Loop para pacientes
        Endereco=num2str(enderecos(p,1));
        Mask=importdata(strcat('C:\Users\Gabriel Borralho\Documents\MEGA\LabPAI\Data_of_patients\',TipoPacientes,'\ID_', Endereco,'\Mask.jpg')); %Caminho da Máscara de cada paciente
        lista = dir(strcat('C:\Users\Gabriel Borralho\Documents\MEGA\LabPAI\Data_of_patients\',TipoPacientes,'\ID_', Endereco,'\corretas\*.txt')); %Caminho do arquivo corretas txt
        
        fid = fopen(strcat('C:\Users\Gabriel Borralho\Documents\MEGA\LabPAI\Data_of_patients\series\series',num2str(janela),'x',num2str(janela),'\',TipoPacientes,'\ST_',TipoPacientes,'_ID_', Endereco,'.txt'),'wt');
        
        %Converter em uma imagem binária (255 e 0)
        for i=1:1:480
            for j=1:1:640
                if Mask(i,j)>=127
                    Mask(i,j)=255;
                else
                    Mask(i,j)=0;
                end

            end
         end

        coluna=1;  linha=1;
        for k=1:1:num_tempos %Loop para imagens de uma mesma paciente
            NomeMatriz=lista(k).name;        
            matriz=importdata(strcat('C:\Users\Gabriel Borralho\Documents\MEGA\LabPAI\Data_of_patients\',TipoPacientes,'\ID_', Endereco,'\corretas\', NomeMatriz));
            for i=1:Tjanela:480-Tjanela
               for j=1:Tjanela:640-Tjanela
                   if Mask(i,j)~=0
                       cond=0;
                       temp_media=0;
                       for x=i:1:i+(Tjanela-1)
                           for y=j:1:j+(Tjanela-1)
                               temp_media=temp_media+matriz(x,y);
                               if Mask(i,j)==0
                                   cond=1;
                               end
                           end
                       end
                       if cond==0
                           temp_media=temp_media/Tjanela^2;
                           ST(linha,coluna)=temp_media; %MUDAR AQUI                           
                           fprintf(fid,'%f ',temp_media); %fica dentro do laço/loop/for
                           linha=linha+1;
                       end
                   end
               end
               
            end        
            coluna=coluna+1;
            linha=1;
            fprintf(fid,'\n'); %fica dentro do laço/loop/for
        end        
        n=n+1;
        disp(strcat('Serie gerada da paciente: ID_', Endereco, ' n=', num2str(n),' classe:' ,TipoPacientes))
        %save(strcat('C:\Users\Gabriel Borralho\Documents\MEGA\LabPAI\Data_of_patients\series\series',num2str(janela),'x',num2str(janela),'\',TipoPacientes,'\ST_',TipoPacientes,'_ID_', Endereco),'ST'); %MUDAR AQUI
        clear ST;
        fclose(fid);
        
        matriz=load(strcat('C:\Users\Gabriel Borralho\Documents\MEGA\LabPAI\Data_of_patients\series\series',num2str(janela),'x',num2str(janela),'\',TipoPacientes,'\ST_',TipoPacientes,'_ID_', Endereco,'.txt'));
        matriz=matriz';
        [a,b]=size(matriz);
        
        fid = fopen(strcat('C:\Users\Gabriel Borralho\Documents\MEGA\LabPAI\Data_of_patients\series\series',num2str(janela),'x',num2str(janela),'\',TipoPacientes,'\ST_',TipoPacientes,'_ID_', Endereco,'.txt'),'wt');
        
        for k=1:1:a
            for p=1:1:b
                fprintf(fid,'%f ',matriz(k,p)); %fica dentro do laço/loop/for
            end
            fprintf(fid,'\n');
        end
        fclose(fid);
    end
    disp(strcat('Series de "',TipoPacientes,'" construidas com sucesso!'))
    TipoPacientes='saudaveis';
end
disp('COMPLETO')
