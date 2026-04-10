# Plano de Ação: Construção do Seed Database Completo para o Projeto IBDN

## 1. Visão Geral do Projeto e Objetivo

O projeto IBDN (Instituto Brasileiro de Desenvolvimento e Natureza) consiste em uma plataforma de gestão de certificações ambientais que permite a concessão de selos de sustentabilidade para empresas de diversos setores. O objetivo deste plano é estabelecer uma estratégia completa para a construção de um banco de dados de seed (dados iniciais) que cubra todos os casos de uso do sistema, proporcionando uma base de dados funcional para desenvolvimento, testes e demonstração.

O seed database proposed shall contain realistic and comprehensive data that simulates a production environment, enabling developers and testers to validate all system functionalities without the need for manual data entry. This includes the creation of multiple user profiles with different permission levels, companies across various industries, seal certifications in different statuses, notification records, and address information. The data shall be structured to respect all database relationships and integrity constraints, ensuring that the seed can be executed reliably at any time during the development lifecycle.

A construção do seed database segue uma abordagem sistemática que considera as dependências entre entidades, a ordem correta de inserção para evitar violations de chave estrangeira, e a criação de cenários de teste que cubram tanto os fluxos principais quanto os casos edge do sistema. Cada categoria de dados foi planejada para incluir diversidade suficiente para validar diferentes comportamentos do sistema, incluindo estados ativos e inativos, registros completos e incompletos, e situações de erro que devem ser tratadas pela aplicação.

## 2. Análise das Tabelas Existentes e Relacionamentos

### 2.1 Entidades Principais e Suas Estruturas

O banco de dados do projeto IBDN é composto por onze tabelas principais que formam a espinha dorsal da aplicação. Cada tabela possui uma estrutura específica diseñada para atender aos requisitos funcionais do sistema, e understanding these structures is fundamental para o planejamento do seed database. A tabela de permissões (ibdn_permissoes) armazena os diferentes tipos de permissões que podem ser atribuídas aos usuários do sistema, contendo apenas o identificador único e o nome da permissão. Esta tabela serve como base para o sistema de controle de acesso, permitindo que diferentes perfis tenham diferentes níveis de autoridade dentro da aplicação.

A tabela de perfis (ibdn_perfis) complementa o sistema de permissões ao agrupar usuários com características semelhantes em grupos lógicos. Cada perfil possui um identificador único e um nome descritivo que o caracteriza, como "administrador", "empresa" ou "admin_master". A relação entre perfis e permissões é estabelecida através da tabela associativa ibdn_perfil_permissoes, que implementa uma relação muitos-para-muitos entre as duas entidades. Esta estrutura permite que um perfil tenha múltiplas permissões e que uma permissão possa ser atribuída a múltiplos perfis, proporcionando flexibility na configuração de níveis de acesso.

A tabela de usuários (ibdn_usuarios) representa os indivíduos que acessam o sistema, contendo informações pessoais e credenciais de autenticação. Cada usuário está associado a um perfil através de uma chave estrangeira, e possui campos para nome, email (único), hash de senha, indicação de ativo/inativo, e configuração de autenticação de dois fatores. A relação entre usuários e empresas é de um-para-um, onde cada empresa possui um usuário responsável vinculado através do campo usuario_id na tabela empresa.

### 2.2 Entidades de Negócio e Suas Relações

As tabelas relacionadas ao negócio principal do IBDN incluem empresa, selo, ramo, e suas tabelas associativas. A tabela empresa armazena as informações corporativas das organizações que buscam ou possuem certificações ambientais, incluindo CNPJ, razão social, nome fantasia, dados do responsável, informações de contato e status de atividade. Cada empresa está necessariamente vinculada a um usuário do sistema que representa o responsável pela gestão da conta.

A tabela de selos (selo) cataloga os diferentes tipos de certificações ambientais oferecidas pelo IBDN, como "Empresa Parceira da Natureza", "Neutro de Carbono", "Hotel ECO Responsável", entre outros. Cada selo possui um nome descritivo, uma sigla única para referência rápida, e uma descrição detalhada dos critérios de certificação. Os selos são concedidos às empresas através da tabela empresa_selo, que registra não apenas a relação entre empresa e selo, mas também metadados importantes como data de emissão, data de expiração, código único do selo, status atual da certificação, e informações sobre o plano contratado.

A tabela de ramos (ramo) classifica as empresas por setor de atuação, permitindo a categorização e busca por segmentos específicos. Esta tabela possui uma relação muitos-para-muitos com empresas através da tabela associativa empresa_ramo, permitindo que uma empresa opere em múltiplos ramos simultaneamente. A tabela de endereços (endereco) armazena as localizações físicas das empresas, com campos detalhados para logradouro, número, bairro, CEP, cidade, UF e complemento.

### 2.3 Entidades de Comunicação e Monitoramento

A tabela de notificações (notificacao) implementa o sistema de comunicação do sistema, permitindo o envio de mensagens às empresas sobre diversos eventos como expiração de selos, necessidade de renovação, alertas de documentação, e comunicados gerais. Cada notificação está vinculada a uma empresa específica e possui campos para mensagem, data de envio, tipo de notificação, e indicação de leitura. O campo tipo permite a categorização das notificações para que o sistema possa filtrar e processar diferentes tipos de mensagens de forma apropriada.

As dependências entre tabelas follows a clear hierarchy que deve ser respeitada durante a inserção de dados. As tabelas base (permissoes, perfis, ramo, selo) não possuem dependências e podem ser preenchidas primeiro. Em seguida, as tabelas associativas (perfil_permissoes) podem ser populadas, seguidas pelas tabelas principais que dependem das bases (usuarios). As tabelas de negócio (empresa, endereco, empresa_ramo, empresa_selo, notificacao) dependem tanto das tabelas base quanto dos usuários e devem ser inseridas por último.

## 3. Identificação Completa dos Casos de Uso do Sistema

### 3.1 Casos de Uso de Gestão de Usuários e Autenticação

O sistema IBDN contempla diversos casos de uso relacionados à gestão de usuários e autenticação que devem ser cobertos pelo seed database. O primeiro caso de uso fundamental é o login de usuário com credenciais válidas, onde o sistema deve validar o email e senha informados, verificar se o usuário está ativo, e retornar o token de autenticação apropriado. Este cenário requer a criação de usuários de teste com senhas hashed corretamente e diferentes statuses de atividade para validar tanto o fluxo positivo quanto os fluxos de erro.

O segundo caso de uso importante é o login com credenciais inválidas, onde o sistema deve rejeitar tentativas de autenticação com email inexistente, senha incorreta, ou usuário inativo. Para validar este comportamento, o seed deve incluir pelo menos um usuário com credenciais conhecidas que seja utilizado nos testes de segurança. O terceiro caso de uso envolve a recuperação de perfil do usuário autenticado, onde o sistema retorna as informações do usuário logado incluindo seu perfil e as permissões associadas, permitindo que a interface adapte seu comportamento de acordo com o nível de acesso.

Os casos de uso avançados incluem a autenticação com dois fatores habilitada, que requer a configuração de usuários específicos com twofactor habilitado para testar este fluxo de segurança adicional. Também deve ser possível testar a alteração de perfil de usuário, verificando que as permissões são atualizadas corretamente quando um usuário muda de perfil. O sistema deve permitir a listagem de todos os usuários com paginação e filtros, o que requer um volume significativo de dados para validar a performance e comportamento da interface de administração.

### 3.2 Casos de Uso de Gestão de Empresas

A gestão de empresas representa o núcleo do negócio do IBDN e contempla múltiplos cenários que devem ser cobertos pelo seed database. O caso de uso de criação de empresa requer que o sistema valide os dados obrigatórios (CNPJ único, razão social), associe a empresa a um usuário responsável, e mantenha o registro com status inicial de atividade. Para este cenário, o seed deve incluir dados de empresas em diferentes estágios de conclusão, algumas com todos os dados preenchidos e outras com campos opcionais missing.

O caso de uso de consulta de empresa permite buscar informações de uma empresa específica pelo ID ou listar todas as empresas com filtros por CNPJ, razão social, ou status de atividade. O seed deve incluir empresas em diferentes situações: ativas e inativas, com e sem selos concedidos, com diferentes quantidades de ramos associados, e em diferentes localizações geográficas. O caso de uso de atualização de empresa permite modificar os dados cadastrais, devendo o sistema validar as mesmas regras de criação e manter o histórico de alterações.

Os casos de uso avançados incluem a associação de ramos à empresa, onde o sistema deve validar que os Ramos existem antes de criar a relação, e a solicitação de selo, onde uma empresa pode iniciar o processo de certificação. O seed deve incluir empresas que já possuem selos concedidos com diferentes datas de expiração (vigentes, próximos do vencimento, e expirados), permitindo testar os fluxos de renovação e expiração de certificações. A consulta de selos concedidos à empresa deve retornar todas as certificações ativas e históricas, com informações completas sobre datas e status.

### 3.3 Casos de Uso de Gestão de Selos e Certificações

O sistema de selos do IBDN contempla casos de uso desde a consulta do catálogo de selos disponíveis até a concessão e gerenciamento de certificações. O caso de uso de consulta de selos disponíveis permite listar todos os selos do catálogo com seus detalhes, incluindo nome, sigla, descrição e critérios de certificação. O seed deve incluir todos os selos definidos no sistema, que já são populados pelo create_initial_data, garantindo que existam opções suficientes para os diferentes tipos de empresas.

O caso de uso de solicitação de selo permite que uma empresa faça o request de certificação, especificando o selo desejado e o plano de validade. O sistema deve validar que a empresa existe, que o selo está disponível, e criar um registro de solicitação com status apropriado. O caso de uso de concessão de selo é restrito a administradores e permite transformar uma solicitação em uma certificação ativa, gerando código único e definindo datas de emissão e expiração.

O gerenciamento de selos concedidos inclui casos de uso para consulta de selos de uma empresa específica, verificação de status de certificação, e alertas para selos próximos do vencimento. O seed deve incluir dados que permitam testar todos estes cenários, incluindo selos em diferentes statuses (solicitado, ativo, expirado,revogado), com diferentes datas de emissão para testar a lógica de alertas e notificações. A documentação de cada certificação também deve ser simulada através do campo documentacao na tabela empresa_selo.

### 3.4 Casos de Uso de Gestão de Ramos e Classificação

Os Ramos de atividade permitem a classificação das empresas por setor de atuação, facilitando a busca e segmentação. O caso de uso de consulta de Ramos disponíveis lista todos os Ramos do catálogo com suas descrições. O seed já inclui dez Ramos iniciais que representam os principais setores atendidos pelo IBDN, desde Hotelaria e Turismo até Tecnologia e Serviços. O caso de uso de associação de Ramos à empresa permite que uma empresa defina em quais setores atua, com suporte à múltiplos Ramos por empresa.

O caso de uso de busca de empresas por Ramo permite identificar todas as empresas certificadas em um determinado setor, útil para relatórios e análises de mercado. O seed deve incluir empresas associadas a diferentes combinações de Ramos para validar esta funcionalidade. A consulta de empresas por múltiplos Ramos simultaneamente também deve ser suportada, onde o sistema retorna empresas que atuam em qualquer ou todos os Ramos especificados.

### 3.5 Casos de Uso de Endereços e Localização

O sistema de endereços permite que cada empresa possua múltiplos locais de operação, armazenando informações detalhadas de localização. O caso de uso de cadastro de endereço associa um novo endereço a uma empresa existente, validando que a empresa existe e que os campos obrigatórios estão presentes. O caso de uso de consulta de endereços de uma empresa lista todos os locais cadastrados, permitindo que uma empresa tenha matriz e filiais distintas.

O caso de uso de atualização de endereço permite modificar os dados de um local específico, mantendo o histórico de alterações. O caso de uso de remoção de endereço exclui um local da empresa, com validação de integridade referencial. O seed deve incluir empresas com diferentes configurações de endereços: algumas com apenas um endereço, outras com múltiplos endereços em diferentes cidades e estados, permitindo testar todos estes cenários de forma abrangente.

### 3.6 Casos de Uso de Notificações e Comunicação

O sistema de notificações automatiza a comunicação com as empresas sobre eventos importantes relacionados às suas certificações. O caso de uso de envio de notificação cria um novo registro de mensagem para uma empresa específica, armazenando a mensagem, data de envio, tipo de notificação e status de leitura inicial. O caso de uso de listagem de notificações retorna as mensagens de uma empresa com suporte a filtros por tipo, data, e status de leitura.

O caso de uso de marcação de notificação como lida atualiza o status de uma mensagem específica, permitindo que o sistema diferencie entre notificações novas e antigas. O caso de uso de notificações não lidas retorna apenas mensagens que o usuário ainda não visualizou, útil para displays de alertas. O seed deve incluir notificações de diferentes tipos (alerta_expiracao, Renovacao_solicitada, Documentacao_pendente, Comunicado_geral), com diferentes status de leitura e em diferentes datas de envio para testar todos os cenários.

## 4. Dados Necessários para Cobrir Cada Caso de Uso

### 4.1 Dados de Permissões e Perfis

O seed database deve incluir um conjunto completo de permissões que cubram todas as ações possíveis no sistema. As permissões fundamentais incluem "admin_master" para acesso total ao sistema, "admin" para administração sem privilégios críticos, e "empresa" para acesso limitado às funcionalidades de gestão da própria empresa. Além destas permissões base, o seed deve incluir permissões granulares como "criar_empresa", "editar_empresa", "visualizar_empresa", "solicitar_selo", "gerenciar_selos", "gerenciar_usuarios", "visualizar_relatorios", e "configurar_notificacoes".

Os perfis do sistema devem ser configurados para associar as permissões de forma lógica e realista. O perfil "admin_master" deve possuir todas as permissões disponíveis, simulando um superusuário do sistema. O perfil "admin" deve possuir permissões de gestão de empresas, selos, e relatórios, mas sem acesso às configurações críticas do sistema. O perfil "empresa" deve possuir permissões limitadas para gestão dos próprios dados, solicitação de selos, e visualização de notificações. O seed deve incluir as associações entre perfis e permissões já estabelecidas na tabela ibdn_perfil_permissoes.

### 4.2 Dados de Usuários para Testes

O seed deve incluir uma diversidade de usuários que permita testar todos os fluxos de autenticação e autorização. O usuário admin_master principal deve ser criado com as credenciais configuradas no arquivo .env (ADMIN_EMAIL e ADMIN_PASSWORD), garantindo que o administrador principal possa acessar o sistema após a execução do seed. Além deste usuário, devem ser criados usuários adicionais para cada perfil existente, com senhas conhecidas e utilizadas nos testes automatizados.

A estrutura de usuários deve incluir pelo menos um usuário ativo e um usuário inativo para cada perfil, permitindo testar a rejeição de logins de usuários desativados. Também deve incluir pelo menos um usuário com autenticação de dois fatores habilitada para testar este fluxo de segurança. Os dados de cada usuário devem incluir nome completo realista, email no formato válido, e associação ao perfil apropriado. A distribuição de usuários deve permitir testar cenários de listagem com paginação, filtros por perfil, e buscas por nome ou email.

### 4.3 Dados de Empresas Realistas

O seed deve incluir um conjunto diversificado de empresas que cubram todos os setores e situações possíveis. Cada empresa deve possui um CNPJ único e válido (formato XX.XXX.XXX/XXXX-XX), razão social completa, nome fantasia quando aplicável, telefone de contato, dados do responsável pela conta (nome e cargo), site quando disponível, e data de cadastro. A distribuição de empresas deve incluir diferentes cenários de status: empresas ativas com certidões vigentes, empresas ativas com selos expirados, empresas inativas, e empresas em processo de certificação.

As empresas devem ser distribuídas geograficamente por diferentes estados do Brasil, com concentrações maiores em centros urbanos como São Paulo, Rio de Janeiro, Minas Gerais, Paraná e Rio Grande do Sul. Esta distribuição permite testar a filtragem por UF e a consulta de empresas por região. Cada empresa deve ter um usuário responsável associado, respeitando a relação um-para-um entre empresa e usuário. A maioria das empresas deve ter endereços cadastrados, com algumas tendo múltiplos endereços em diferentes localidades.

### 4.4 Dados de Selos e Certificações

O seed deve incluir todas as certificações possíveis para cada empresa, cobrindo diferentes statuses e temporalidades. Para cada tipo de selo disponível no catálogo (EPN, NC, PES, HER, ER, CC), deve haver empresas em diferentes situações: algumas nunca terem solicitado o selo, outras com solicitação em andamento, outras com certificação ativa, e outras com certificação expirada. Esta distribuição permite testar todos os fluxos de ciclo de vida de uma certificação.

As certificações ativas devem ter diferentes datas de emissão e expiração para cobrir cenários de alertas. Devem existir selos com mais de um ano de validade remaining, selos próximos do vencimento (dentro de 30 dias), e selos recentemente expirados. Cada certificação ativa deve ter um código de selo único gerado, simulando a identificação real das certificações. O campo documentacao deve incluir referências a documentos simulados, e o campo alerta_enviado deve indicar se notificações de expiração já foram enviadas.

### 4.5 Dados de Ramos e Associações

Os Ramos iniciais já são populados pelo create_initial_data, mas o seed deve incluir as associações entre empresas e Ramos de forma realista. Cada empresa deve estar associada a pelo menos um Ramo principal que representa sua atividade principal, e pode estar associada a Ramos adicionais que representam atividades secundárias. A distribuição deve refletir o mercado real, com maior concentração nos setores de Tecnologia e Serviços, Alimentos e Bebidas, e Construção Civil e Imobiliário.

### 4.6 Dados de Endereços

Cada empresa ativa deve ter pelo menos um endereço cadastrado, com a maioria tendo apenas um endereço (matriz). Um subconjunto de empresas deve ter múltiplos endereços (filiais), permitindo testar a gestão de múltiplos locais. Os endereços devem seguir o formato brasileiro completo, incluindo logradouro, número, complemento quando aplicável, bairro, CEP (formato XXXXX-XXX), cidade e UF. A distribuição geográfica deve cobrir diferentes regiões do Brasil, com cities representative de cada estado.

### 4.7 Dados de Notificações

O seed deve incluir um histórico de notificações que permita testar todos os fluxos de comunicação. As notificações devem ser distribuídas por tipo, com代表性 de cada categoria: alertas de expiração próximos, comunicados de renovação necessária, mensagens sobre documentação pendente, e comunicados gerais do IBDN. Cada empresa deve ter entre zero e cinco notificações, com algumas empresas tendo notificações não lidas (importantes para testar o sistema de alertas) e outras tendo todas as notificações já lidas.

As notificações devem ter datas de envio distribuídas ao longo do último ano, simulando uma histórico realista de comunicação. Devem existir notificações recentes (últimos 7 dias), notificações do último mês, e notificações mais antigas. A tabela deve incluir notificações de diferentes empresas, permitindo testar a filtragem por empresa. O campo tipo deve seguir uma convenção consistente (alerta_expiracao, Renovacao_solicitada, Documentacao_pendente, Comunicado_geral, among others).

## 5. Estrutura do Seed com Dados Realistas e Completos

### 5.1 Arquitetura do Script de Seed

O seed database deve ser implementado como um script Python modular que pode ser executado de forma independente ou integrado ao processo de inicialização da aplicação. A estrutura recomendada utiliza uma abordagem de classes ou funções especializadas para cada categoria de dados, com funções de helpers para geração de dados aleatórios e validação de dependências. O script deve ser idempotente, permitindo múltiplas execuções sem causar duplicações ou errors de integridade.

O script principal (seed_db.py) deve seguir a ordem de inserção correta: primeiro limpar dados existentes (opcional e controlado por flag), depois inserir permissões, perfis, Ramos e selos base, em seguida criar usuários, e por último inserir empresas, endereços, associações e notificações. Cada etapa deve ser envolvida em uma transação separada para permitir rollback em caso de erro, e deve incluir logs informativos que indicam o progresso da execução.

A estrutura de diretórios recomendada coloca o script de seed em uma pasta dedicada (app/database/seed/) com módulos separados para cada categoria de dados. O arquivo principal importa todos os módulos e executa a sequência completa, enquanto módulos individuais podem ser importados para testes parciais. Esta estrutura facilita a manutenção e extensão do seed ao longo do tempo, permitindo adicionar novos cenários sem modificar a estrutura global.

### 5.2 Geração de Dados Faker

A geração de dados realistas deve utilizar a biblioteca Faker (python-faker) para criar nomes, endereços, telefones e outros dados que sigam padrões brasileiros. A configuração do Faker deve incluir locale "pt_BR" para garantir que os dados seguem convenções brasileiras, incluindo formatação de CPFs e CNPJs, endereços brasileiros, e nomes compatíveis com a cultura local.

Para CNPJs, recomenda-se criar uma função helper que gera CNPJs válidos utilizando o algoritmo de dígitos verificadores, garantindo que o sistema de validação aceite os dados do seed. Similarmente, CEPs devem ser gerados a partir de ranges válidos de cada estado, preferencialmente utilizando CEPs reais de cities representativos. Os telefones devem seguir o formato brasileiro com código de área (XX) XXXX-XXXX ou XXXXX-XXXX, dependendo se é fixo ou móvel.

### 5.3 Estrutura de Dados por Categoria

A categoria de permissões deve incluir as permissões base e granulares em um arquivo dedicado (seed_permissions.py), com funções para criar permissões, associar a perfis, e verificar existência prévia. Cada permissão deve ter um nome descritivo e único, seguindo uma convenção de nomenclatura consistente como "acao_recurso" (ex: "criar_empresa", "visualizar_selo").

A categoria de perfis deve incluir a criação dos perfis base e a associação com permissões em um arquivo dedicado (seed_profiles.py). A ordem de execução deve garantir que as permissões existam antes de criar as associações. Os perfis devem ser criados com IDs previsíveis para facilitar a referência em outros módulos do seed.

A categoria de usuários deve incluir a criação de usuários de teste em um arquivo dedicado (seed_users.py), com funções para criar usuários admin, usuários empresa, e verificar existência prévia. Cada usuário deve ter um perfil associado, e deve ser possível criar usuários com senhas conhecidas para testes automatizados. A geração de senhas deve utilizar a mesma função de hash utilizada pela aplicação.

A categoria de empresas deve ser a mais complexa, com um arquivo dedicado (seed_empresas.py) que cria empresas realistas com todos os dados necessários. A função principal deve criar um número configurável de empresas, distribuídas por diferentes cenários de status, setores, e localizações. Para cada empresa criada, devem ser criados automaticamente o usuário associado, endereços, associações de Ramos, e um subconjunto de notificações.

## 6. Ordem de Inserção e Dependências

### 6.1 Sequência de Execução

A ordem de inserção é critical para evitar violations de chave estrangeira e garantir a integridade dos dados. A sequência completa de execução deve seguir a seguinte ordem: (1) permissões, (2) perfis, (3) Ramos, (4) selos, (5) perfil_permissoes, (6) usuários, (7) empresas, (8) endereços, (9) empresa_ramo, (10) empresa_selo, e (11) notificações.

Cada etapa deve verificar a existência dos dados antes de inserir, evitando duplicações em execuções subsequentes do seed. O script deve incluir um mecanismo de verificação que permite determinar se os dados já foram populados, retornando imediatamente se todas as tabelas já contêm dados. Esta abordagem permite que o seed seja executado múltiplas vezes sem causar problemas, seja durante o desenvolvimento ou em ambientes de produção.

### 6.2 Transações e Rollback

Cada categoria de dados deve ser envolvida em uma transação separada que pode ser confirmada ou revertida individualmente. Em caso de erro durante a inserção de uma categoria, o rollback deve ser executado para desfazer todas as operações da etapa com falha, permitindo que o seed possa ser executado novamente após a correção do problema. O log deve registrar claramente qual etapa falhou e o motivo do erro.

O tratamento de erros deve ser abrangente o suficiente para capturar falhas de conexão, violations de integridade, e erros de validação. Cada exception deve ser logada com detalhes suficientes para diagnóstico, incluindo os parâmetros que foram utilizados na operação que falhou. Após um erro, o script deve finalizar de forma controlada sem deixar conexões abertas ou transações pendentes.

### 6.3 Verificação Pós-Execução

Após a conclusão de todas as etapas, o seed deve executar verificações para garantir que os dados foram inseridos corretamente. As verificações mínimas incluem: contagem de registros em cada tabela, verificação de chaves estrangeiras válidas, e confirmação de que usuários possuem perfis associados. O resultado destas verificações deve ser logado e utilizado para determinar se o seed foi executado com sucesso.

O script deve gerar um relatório final que indica o número de registros inseridos em cada categoria, o tempo de execução de cada etapa, e warnings sobre situações inesperadas (como registros órfãos ou associações faltantes). Este relatório pode ser utilizado para auditoria e para verificar que o seed está produzindo os resultados esperados.

## 7. Divisão por Categorias e Responsabilidades

### 7.1 Módulo de Permissões e Perfis

O módulo de permissões e perfis (seed_permissions_profiles.py) é responsável por criar a base do sistema de controle de acesso. Este módulo define todas as permissões disponíveis no sistema, cria os perfis padrão, e estabelece as associações entre perfis e permissões. A execução deste módulo é prerequisito para todos os outros módulos, pois os usuários e empresas dependem dos perfis para funcionar corretamente.

As permissões criadas por este módulo devem cobrir todas as ações possíveis no sistema: gerenciamento de usuários, gerenciamento de empresas, solicitação de selos, concessão de selos, gerenciamento de Ramos, envio de notificações, e visualização de relatórios. Cada permissão deve ter um nome descritivo e único que permita identificar facilmente a ação que ela representa.

### 7.2 Módulo de Catálogos

O módulo de catálogos (seed_catalogos.py) é responsável por criar os dados de referência do sistema, incluindo Ramos de atividade e selos de certificação. Estes dados são relativamente estáveis e não mudam frequentemente no dia a dia do sistema, sendo considerados dados de configuração. O módulo deve verificar a existência prévia de cada registro para evitar duplicações em execuções subsequentes.

Os Ramos devem incluir os dez setores definidos inicialmente, cada um com uma descrição detalhada que explica o foco da certificação naquele setor. Os selos devem incluir os seis tipos de certificação disponíveis, com nomes, siglas e descrições completas. Este módulo deve ser executado antes do módulo de empresas, pois as empresas serão associadas aos Ramos e solicitarão selos do catálogo.

### 7.3 Módulo de Usuários

O módulo de usuários (seed_usuarios.py) é responsável por criar os usuários do sistema que representam pessoas reais ou jurídicas que acessam a plataforma. Este módulo cria o usuário admin_master com credenciais do arquivo .env, e também cria usuários adicionais para testes com diferentes perfis e statuses. Cada usuário deve ter um email único e válido, um nome completo, e estar associado a um perfil existente.

A criação de usuários deve ser feita antes da criação de empresas, pois cada empresa requer um usuário responsável vinculado. O módulo deve gerar senhas hashed utilizando a mesma função utilizada pela aplicação, garantindo que os usuários possam fazer login normalmente após o seed. Recomenda-se criar uma lista de usuários de teste com senhas conhecidas que podem ser utilizadas em testes automatizados.

### 7.4 Módulo de Empresas e Relacionamentos

O módulo de empresas (seed_empresas.py) é o mais complexo e extenso do seed database, responsável por criar todas as empresas do sistema e seus relacionamentos. Este módulo deve ser executado após os módulos de catálogos e usuários, pois depende de ambos para criar as associações corretas. Para cada empresa criada, o módulo deve automaticamente criar o usuário responsável, os endereços, as associações de Ramos, e um histórico de selos e notificações.

A geração de empresas deve seguir uma estratégia de cenários que cubra todos os casos de uso identificados. Cada empresa deve ter dados realistas e completos, incluindo todas as informações obrigatórias e uma variedade de campos opcionais. A distribuição de empresas por setor, localização geográfica, e status de certificação deve ser balanceada o suficiente para permitir testes significativos de todas as funcionalidades.

### 7.5 Módulo de Endereços

O módulo de endereços (seed_enderecos.py) pode ser integrado ao módulo de empresas ou executado separadamente, dependendo da estratégia de implementação escolhida. Se executado separadamente, deve ser executado após o módulo de empresas e antes do módulo de notificações. A responsabilidade principal é garantir que cada empresa tenha pelo menos um endereço cadastrado, com suporte a múltiplos endereços para empresas que possuem filiais.

Os endereços devem seguir o formato brasileiro completo e devem ser geograficamente realistas, com CEPs válidos e localizações em cities reais. A distribuição deve cubrir diferentes estados e regiões do Brasil, permitindo testar funcionalidades de busca por localização. Este módulo não depende de nenhuma tabela específica além de empresa, sendo relativamente independente no contexto do seed.

### 7.6 Módulo de Notificações

O módulo de notificações (seed_notificacoes.py) é responsável por criar o histórico de comunicações do sistema, simulando mensagens que teriam sido enviadas ao longo do tempo. Este módulo deve ser executado por último, pois depende de todas as outras tabelas já estarem populadas. Cada notificação deve estar associada a uma empresa existente e deve ter dados realistas de mensagem, tipo, e data de envio.

A geração de notificações deve criar um histórico que cubra diferentes cenários: notificações recentes e antigas, diferentes tipos de comunicação, e diferentes status de leitura. Deve haver um equilíbrio entre empresas com muitas notificações e empresas com poucas ou nenhuma, simulando diferentes padrões de uso do sistema. Este módulo é fundamental para testar a interface de notificações e os fluxos de comunicação automatizados.

## 8. Cronograma de Implementação Sugerido

### 8.1 Fase 1: Estrutura Base

A primeira fase de implementação deve focar na criação da estrutura base do seed database, incluindo a criação dos arquivos de módulo, a configuração do Faker, e a implementação das funções helper de utilidade. O deliverable desta fase é um script funcional que consegue executar sem erros e populates as tabelas de permissões, perfis, Ramos e selos. O tempo estimado para esta fase é de dois dias de desenvolvimento.

Os principais riscos desta fase incluem a configuração inicial do ambiente (acesso ao banco de dados, variáveis de ambiente) e a definição das estruturas de dados necessárias. Recomenda-se iniciar com um script simples que apenas cria permissões e perfis, validando a conexão com o banco de dados antes de prosseguir para dados mais complexos.

### 8.2 Fase 2: Módulo de Usuários e Empresas

A segunda fase deve implementar os módulos de usuários e empresas, que são os mais críticos para o funcionamento do sistema. O deliverable é um script que cria usuários com diferentes perfis e empresas com dados realistas, incluindo as associações básicas entre entidades. O tempo estimado para esta fase é de três dias de desenvolvimento.

Os principais desafios incluem a geração de CNPJs válidos, a criação de dados que passam nas validações do Pydantic, e o balanceamento da distribuição de empresas por cenários. Recomenda-se implementar primeiro uma versão simplificada com um número pequeno de empresas, e depois estender para o volume completo necessário para os testes.

### 8.3 Fase 3: Módulos Complementares

A terceira fase deve implementar os módulos complementares de endereços e notificações, completando o seed database. O deliverable é um script completo que popula todas as tabelas do sistema com dados realistas e completos. O tempo estimado para esta fase é de dois dias de desenvolvimento.

### 8.4 Fase 4: Validação e Documentação

A quarta fase deve focar na validação do seed database e na documentação do resultado. O deliverable é um relatório de validação que confirma que todos os casos de uso podem ser testados com os dados criados, e a documentação do código do seed. O tempo estimado para esta fase é de um dia.

A validação deve incluir a execução de testes manuais que verificam cada caso de uso identificado, confirmando que os dados existentes são suficientes para cobrir o cenário. A documentação deve incluir instruções de uso, descrição de cada módulo, e informações sobre como estender o seed no futuro.

## 9. Conclusão e Próximos Passos

O plano de ação detalhado apresentado neste documento fornece uma estrutura abrangente para a construção do seed database completo do projeto IBDN. A implementação deve seguir a ordem de fases estabelecida, começando pela estrutura base e progredindo até a validação final. O resultado será um banco de dados de seed funcional que cobre todos os casos de uso identificados, possibilitando o desenvolvimento e teste eficientes de todas as funcionalidades do sistema.

A execução deste plano requer coordenação entre as equipes de backend, QA, e produto para garantir que os dados criados atendam às necessidades de todos os stakeholders. Recomenda-se agendar revisões periódicas durante a implementação para validar que os dados estão alinhados com as expectativas e para fazer ajustes necessários no escopo. O seed database成品 deve ser tratado como parte integral do código do projeto, com versionamento e revisões apropriadas.

Os próximos passos imediatos incluem a criação da estrutura de diretórios para os módulos do seed, a configuração inicial do Faker com locale brasileiro, e a implementação do primeiro módulo (permissões e perfis). Após a conclusão do seed database, recomenda-se criar testes automatizados que validem periodicamente que os dados estão íntegros e que novos desenvolvimentos não quebram a funcionalidade existente.
