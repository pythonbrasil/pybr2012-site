# encoding: utf-8
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models


class Migration(DataMigration):

    def forwards(self, orm):
        tracks = [
            ('Core & Interpreters', 'Core & Interpretadores',
             'The language, CPython, PyPy, Jython, IronPython, bindings, standard library, optimizations',
             'A linguagem, CPython, PyPy, Jython, IronPython, bindings, bibliotaca padrão, otimizações'),
            ('Games & Multimedia', 'Jogos & Multimídia',
             'Games, multimedia, image and video processing, interactivity, digital TV',
             'Jogos, multimídia, processamento de imagens e vídeo, interatividade, TV digital'),
            ('Embedded Systems & Mobile', 'Sistemas embarcados e móveis',
             'Microncontrollers, wireless sensor networks, mobile applications',
             'Microcontroladores, redes de sensores sem fio, aplicativos para celular'),
            ('GUI Programming', 'GUI',
             'GUI libraries, human-machine interface',
             'Bibliotecas GUI, interface homem-máquina '),
            ('Business', 'Negócios',
             'Entrepreneurship, innovation, success cases',
             'Empreendedorismo, inovação, casos de sucesso'),
            ('Databases', 'Banco de dados',
             'Databases, information retrieval, information systems',
             'Bancos de dados, recuperação de informação, sistemas de informação'),
            ('Science', 'Python na ciência',
             'Scientific computing, natural language processing, artificial intelligence, computer simulation',
             'Computação científica, processamento de linguagem natural, inteligência artificial, simulação computacional'),
            ('Python in society', 'Python na sociedade',
             'Communities, education, open data, government, art',
             'Comunidades, educação, dados abertos, governo, artes'),
            ('Web Frameworks', 'Frameworks Web',
             'Frameworks for Web development, libraries, applications',
             'Frameworks para desenvolvimento Web, bibliotecas, aplicações'),
            ('Cloud computing', 'Computação na nuvem',
             'Cloud computing, virtual machines, elasticity, infrastructure',
             'Computação na nuvem, máquinas virtuais, elasticidade, infraestrutura'),
            ('SysAdmin & DevOp', 'SysAdmin & DevOp',
             'Systems administration, infrastructure management',
             'Administração de sistemas, gerenciamento de infraestrutura'),
            ('Networks', 'Redes de computadores',
             'Distributed systems, network protocols, security',
             'Sistemas distribuídos, protocolos de rede, segurança'),
            ('Django', 'Django',
             'The framework, applications, libraries',
             'O framework, aplicações, bibliotecas'),
            ('Plone', 'Plone',
             'The framework, applications, libraries',
             'O framework, aplicações, bibliotecas'),
            ('Tools & methodology', 'Ferramentas e metodologias',
             'Good practices, design patterns, tests, documentation, packaging',
             'Boas práticas, design patterns, testes, documentação, empacotamento'),
            ('Other', 'Outra',
             'Does not fit in other options',
             'Não se encaixa nas demais opções'),
        ]
        for info in tracks:
            track = orm.Track(name_en_us=info[0], name_pt_br=info[1],
                              description_en_us=info[2],
                              description_pt_br=info[3])
            track.save()

    def backwards(self, orm):
        raise RuntimeError("Cannot reverse this migration.")

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 8, 22, 21, 50, 51, 913320)'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 8, 22, 21, 50, 51, 913235)'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'schedule.session': {
            'Meta': {'object_name': 'Session'},
            'audience_level': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'speakers': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'symmetrical': 'False'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'proposed'", 'max_length': '10'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'track': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['schedule.Track']"}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'schedule.track': {
            'Meta': {'object_name': 'Track'},
            'description_en_us': ('django.db.models.fields.CharField', [], {'max_length': '2000'}),
            'description_pt_br': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name_en_us': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name_pt_br': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['schedule']
