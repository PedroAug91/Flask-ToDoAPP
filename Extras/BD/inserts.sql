use FlaskToDo;

insert into Usuario (id_usuario, nome, email, senha) values
('1', 'Fulano 1', 'fulano1@gmail.com', '1'),
('2', 'Fulano 2', 'fulano2@gmail.com', '2'),
('3', 'Fulano 3', 'fulano3@gmail.com', '3'),
('4', 'Fulano 4', 'fulano4@gmail.com', '4'),
('5', 'Fulano 5', 'fulano5@gmail.com', '5');

insert into Tarefa (id_tarefa, descricao, ativo, id_usuario) values
('1', 'Descricao 1', 1, '1'),
('2', 'Descricao 2', 1, '2'),
('3', 'Descricao 3', 1, '3'),
('4', 'Descricao 4', 1, '4'),
('5', 'Descricao 5', 1, '5'),
('6', 'Descricao 6', 1, '1'),
('7', 'Descricao 7', 1, '1');