class GraphController < ApplicationController
  def index
  	#Positividade politicos

  end

  def politico_referenciado_acumulado
    @auto_complete = auto_complete_personalities
    
    @result_days = ["ola"]
    @result_references = [0]

    if params[:search]!= nil
      aux = 0
      Dir.glob("./files_eadw/politicos_mais_falados/*.txt").each do |file|
        p file
        File.open(file).each_line do |line|
          puts "line split: ", line.split(":")[0]
          puts "params",  params[:search]
          if line.split(":")[0] == params[:search]
            @result_references << @result_references[aux] + line.split(":")[1].to_i 
            @result_days << file.split('.txt')[0].split('__')[1]
            aux = aux + 1
          end
        end
      end
    end
  end

  def politico_referenciado
    @auto_complete = auto_complete_personalities
    
    @result_days = []
    @result_references = []

    if params[:search]!= nil
      Dir.glob("./files_eadw/politicos_mais_falados/*.txt").each do |file|
        p file
        File.open(file).each_line do |line|
          puts "line split: ", line.split(":")[0]
          puts "params",  params[:search]
          if line.split(":")[0] == params[:search]
            @result_references << line.split(":")[1].to_i 
            @result_days << file.split('.txt')[0].split('__')[1]
          end
        end
      end
    end
  end

  def dois_politicos
    @auto_complete = auto_complete_personalities
    if params[:search1] && params[:search2] 
      @results = `python ./python_proj/main/scripdoispoliticos.py #{params[:search1].gsub(" ","_")} #{params[:search2].gsub(" ","_")}`
      
      results = @results.split("\n")
      @results = results[2].to_i
    end
  end

  def site_politicos
    @auto_complete = auto_complete_personalities

    if params[:search]!=nil
      puts params[:search].gsub(" ","_")
      @results = `python ./python_proj/main/scriptpesquisa.py #{params[:search].gsub(" ","_")}`

      results = @results.split("\n")
      results.shift
      @results = results
    end
  end

  def auto_complete_personalities
    personalities_file = './files_eadw/personalities/personalities.txt'
    
    people = File.read(personalities_file).split(/\":\d*,\"/)
    people[0] = people.first.split(/\{\"[A-z]*\":\{\"/)[1]
    people[ people.size - 1 ] = people.last.split(/\":\d*\}\}/)[0]

    people2 = []
    people.each do |person|
      people2 << person.strip
    end
    return people2
  end

  def all_days
    @get_dias = get_items_dia

    days = get_all_days_info
    @neutras = days[:neutras]
    @positivas = days[:positivas]
    @negativas = days[:negativas]
  end

  def mais_positivo
    @auto_complete = get_items_positivo

  	@pos = vars_positividade_politicos[:nomes]
  	@pos_val = vars_positividade_politicos[:valores]
    @dia = vars_positividade_politicos[:dia]
  end

  def mais_referenciado
    @auto_complete = get_items_mais_falado

  	@pos = vars_referenciado_politicos[:nomes]
  	@pos_val = vars_referenciado_politicos[:valores]
    @dia = vars_referenciado_politicos[:dia]
  end

  def positividade_dia
    @auto_complete = get_items_dia

    vars = vars_positividade_dia(params)
  	@not_pos = vars[:positivas]
  	@not_neg = vars[:negativas]
  	@not_neu = vars[:neutras]
    @dia = vars[:dia]
  end


  def vars_positividade_politicos
    if(params[:search]!=nil)
      result = {:nomes => [],:valores => []}
      file_path = "./files_eadw/politcos_positividade/PositividadePoliticos__#{params[:search]}.txt"
      f = File.open(file_path,'r')
      result[:dia] = file_path.split('__')[1].split('.')[0]
      f.each_line do |line|
        vars = line.split(':')
        result[:nomes] << vars[0]
        result[:valores] << vars[1].to_i
     end
    else
        result = {:nomes => [],:valores => []}
        file_path = "./files_eadw/politcos_positividade/PositividadePoliticos__15May2013.txt"
        f = File.open(file_path,'r')
        result[:dia] = file_path.split('__')[1].split('.')[0]
        f.each_line do |line|
          vars = line.split(':')
          result[:nomes] << vars[0]
          result[:valores] << vars[1].to_i
       end
    end
    return result
  end

  def vars_referenciado_politicos 
    if(params[:search]!=nil)
      result = {:nomes => [],:valores => []}
      file_path = "./files_eadw/politicos_mais_falados/PoliticosMaisFalados__#{params[:search]}.txt"
      f = File.open(file_path,'r')
      result[:dia] = file_path.split('__')[1].split('.')[0]

      f.each_line do |line|
      vars = line.split(':')
      result[:nomes] << vars[0]
      result[:valores] << vars[1].to_i
      end 

    else
      result = {:nomes => [],:valores => []}
      file_path = "./files_eadw/politicos_mais_falados/PoliticosMaisFalados__15May2013.txt"
      f = File.open(file_path,'r')
      result[:dia] = file_path.split('__')[1].split('.')[0]

      f.each_line do |line|
        vars = line.split(':')
        result[:nomes] << vars[0]
        result[:valores] << vars[1].to_i
      end
    end
    return result
  end

  def vars_positividade_dia params
    if(params[:search]!=nil)
      result = {:negativas => 0,:positivas => 0, :neutras => 0}
      file_path = "./files_eadw/dias_positividade/PosividadeDoDia__#{params[:search]}.txt"
      result[:dia] = file_path.split('__')[1].split('.')[0]

      f = File.open(file_path,'r')
      f.each_line do |line|
        splited_line = line.split(':')
        if splited_line[0] == "positivas"
          result[:positivas] = splited_line[1]
        elsif splited_line[0] == "neutras"
          result[:neutras] = splited_line[1]
        else
          result[:negativas] = splited_line[1]
        end
      end
    else
      result = {:negativas => 0,:positivas => 0, :neutras => 0}
      file_path = "./files_eadw/dias_positividade/PosividadeDoDia__15May2013.txt"
      result[:dia] = file_path.split('__')[1].split('.')[0]

      f = File.open(file_path,'r')
      f.each_line do |line|
        splited_line = line.split(':')
        if splited_line[0] == "positivas"
          result[:positivas] = splited_line[1]
        elsif splited_line[0] == "neutras"
          result[:neutras] = splited_line[1]
        else
          result[:negativas] = splited_line[1]
        end
      end
    end
    return result
  end

  def get_all_days_info
    days = {:negativas => [], :positivas => [], :neutras => []}
    Dir.glob("./files_eadw/dias_positividade/*.txt").each do |file|
      File.open(file).each_line do |line|
        splited_line = line.split(':')
        p splited_line[0]
        p splited_line[1]
        if(splited_line[0]=="positivas")
          days[:positivas] << splited_line[1].to_i
        elsif(splited_line[0]=="neutras")
          days[:neutras] << splited_line[1].to_i
        else
          days[:negativas] << splited_line[1].to_i
        end
      end
    end
    return days
  end

  def get_items_dia
    auto_complete = []
     Dir.glob("./files_eadw/dias_positividade/*.txt").each do |file|
      auto_complete << file.split('.txt')[0].split('__')[1]
     end
     return auto_complete
  end
  def get_items_mais_falado
    auto_complete = []
     Dir.glob("./files_eadw/politicos_mais_falados/*.txt").each do |file|
      auto_complete << file.split('.txt')[0].split('__')[1]
     end
     return auto_complete
  end
    def get_items_positivo
    auto_complete = []
     Dir.glob("./files_eadw/politcos_positividade/*.txt").each do |file|
      auto_complete << file.split('.txt')[0].split('__')[1]
     end
     return auto_complete
  end


end
