import pandas as pd
from pyvis.network import Network
import networkx as nx



#==========Read CSV files===============
df_author = pd.read_csv('author.csv',encoding = 'ISO-8859-1')
df_year = pd.read_csv('year.csv',encoding = 'ISO-8859-1')
df_keyword = pd.read_csv('keyword.csv',encoding = 'ISO-8859-1')
df_publication = pd.read_csv("publication.csv", engine='python',skip_blank_lines=True,error_bad_lines=False,warn_bad_lines=False)
df_venue = pd.read_csv("venue.csv", engine='python',skip_blank_lines=True,error_bad_lines=False,warn_bad_lines=False)
df_Publication_keywords = pd.read_csv('Publication_keywords.csv',encoding = 'ISO-8859-1')
df_Publication_author = pd.read_csv('Publication_author.csv',encoding = 'ISO-8859-1')
df_Publication_year = pd.read_csv('Publication_year.csv',encoding = 'ISO-8859-1')
df_Publication_venue = pd.read_csv('Publication_venue.csv',encoding = 'ISO-8859-1',skip_blank_lines=True,error_bad_lines=False,warn_bad_lines=False)
#renommage dans le dataframe df_publication_venue de la colonne d_venue en id_venue
df_Publication_venue.rename(columns={'d_venue': 'id_venue'}, inplace=True)




#----affichage des graphes -----
def graphe(df,src,dest):
    G = nx.from_pandas_edgelist(df, src, dest)
    got_net = Network(height="100%", width="100%", bgcolor="#bdc3c7", font_color="#2c3e50",heading="Graphe :")
    got_net.from_nx(G)
    donnees = got_net.get_adj_list()
    for node in got_net.nodes:
        node["value"] = len(donnees[node["id"]])
    got_net.force_atlas_2based()
    for i in range(len(got_net.nodes)):
        if i==0:
            dtt=Info_node(src , got_net.nodes[i]["id"])
            got_net.nodes[i]["label"] = dtt[1]
            got_net.nodes[i]["font"]["color"] = "#e67e22"
            got_net.nodes[i]["font"]["size"] = 20
            got_net.nodes[i]["color"] = "#f39c12"
            got_net.nodes[i]["title"] = "les donnees:<br>" + "".join(dtt[0])
            continue
        dts=Info_node(dest , got_net.nodes[i]["id"])
        got_net.nodes[i]["label"] = dts[1]
        got_net.nodes[i]["font"]["color"] = "#2c3e50"
        got_net.nodes[i]["color"] = "#2980b9"
        got_net.nodes[i]["title"] = "les donnees:<br>" + "".join(dts[0])

    got_net.save_graph('static/graphe.html')



def get_id_author(aut_name):
    df_at = df_author.loc[df_author.name_author.str.contains(aut_name, na=False),['id_author']]
    return df_at['id_author'].values[0]

def get_id_pub(pub_name):
    df_pp = df_publication.loc[df_publication.article_title.str.contains(pub_name),['id_publication']]
    return df_pp['id_publication'].values[0]

def get_id_venue(names):
    df_vv = df_venue.loc[df_venue.name_venue.isin(names.split(",")),['id_venue']]
    return df_vv['id_venue'].values.tolist()



#------------------fonctions--------------------
def Author(dict):
    df_copy = pd.merge(df_author,df_Publication_author, left_on = 'id_author', right_on = 'id_author', how = 'inner')
    if "publication" in dict:
        df_copy= pd.merge(df_copy,df_publication, left_on = 'id_publication', right_on = 'id_publication', how = 'inner')
        df_copy = df_copy.loc[df_copy.id_publication==get_id_pub(dict["publication"])]
        source="id_publication"
    if "venue" in dict:
        df_copy = pd.merge(df_copy, df_Publication_venue, left_on='id_publication', right_on='id_publication',how='inner')
        df_copy = df_copy.loc[df_copy.id_venue.isin(get_id_venue(dict["venue"]))]
        source = "id_venue"
    if "keyword" in dict:
        df_copy = pd.merge(df_copy, df_Publication_keywords, left_on='id_publication',right_on='id_publication', how='inner')
        df_copy = df_copy.loc[df_copy.keyword.isin(dict["keyword"].split(","))]
        source = "keyword"
    if "year" in dict:
        df_copy = pd.merge(df_copy, df_Publication_year, left_on='id_publication', right_on='id_publication',how='inner')
        df_copy = df_copy.loc[df_copy.id_year == 'id_' + dict["year"]]
        source = "id_year"

    graphe(df_copy.head(500), source, 'id_author')
    return df_copy
    


def Publication(dict):
    df_copy = df_publication.copy()
    if "author" in dict:
        df_copy= pd.merge(df_copy,df_Publication_author, left_on = 'id_publication', right_on = 'id_publication', how = 'inner')
        df_copy = df_copy.loc[df_copy.id_author==get_id_author(dict["author"])]
        source = "id_author"
    if "venue" in dict:
        df_copy = pd.merge(df_copy, df_Publication_venue, left_on='id_publication', right_on='id_publication',how='inner')
        df_copy = df_copy.loc[df_copy.id_venue.isin(get_id_venue(dict["venue"]))]
        source = "id_venue"
    if "keyword" in dict:
        df_copy = pd.merge(df_copy, df_Publication_keywords, left_on='id_publication',right_on='id_publication', how='inner')
        df_copy = df_copy.loc[df_copy.keyword.isin(dict["keyword"].split(","))]
        source = "keyword"
    if "year" in dict:
        df_copy = pd.merge(df_copy, df_Publication_year, left_on='id_publication', right_on='id_publication',how='inner')
        df_copy = df_copy.loc[df_copy.id_year == 'id_' + dict["year"]]
        source = "id_year"

    graphe(df_copy.head(500), source, 'id_publication')
    return df_copy

def Keywords(dict):
    df_copy = df_Publication_keywords.copy()
    if "author" in dict:
        df_copy = pd.merge(df_copy, df_Publication_author, left_on='id_publication',right_on='id_publication', how='inner')
        df_copy = df_copy.loc[df_copy.id_author == get_id_author(dict["author"])]
        source = "id_author"
    if "publication" in dict:
        df_copy = df_copy.loc[df_copy.id_publication == get_id_pub(dict["publication"])]
        source = "id_publication"
    if "venue" in dict:
        df_copy = pd.merge(df_copy, df_Publication_venue, left_on='id_publication',right_on='id_publication', how='inner')
        df_copy = df_copy.loc[df_copy.id_venue.isin(get_id_venue(dict["venue"]))]
        source = "id_venue"
    if "year" in dict:
        df_copy = pd.merge(df_copy, df_Publication_year, left_on='id_publication', right_on='id_publication',how='inner')
        df_copy = df_copy.loc[df_copy.id_year == 'id_' + dict["year"]]
        source = "id_year"

    graphe(df_copy.head(500), source, 'keyword')
    return df_copy


def Venue(dict):
    df_copy = pd.merge(df_venue,df_Publication_venue,left_on='id_venue', right_on='id_venue',how='inner')
    if "author" in dict:
        df_copy = pd.merge(df_copy, df_Publication_author, left_on='id_publication', right_on='id_publication',how='inner')
        df_copy = df_copy.loc[df_copy.id_author == get_id_author(dict["author"])]
        source = "id_author"
    if "publication" in dict:
        df_copy = df_copy.loc[df_copy.id_publication == get_id_pub(dict["publication"])]
        source = "id_publication"
    if "keyword" in dict:
        df_copy = pd.merge(df_copy, df_Publication_keywords, left_on='id_publication',right_on='id_publication', how='inner')
        df_copy = df_copy.loc[df_copy.keyword.isin(dict["keyword"].split(","))]
        source = "keyword"
    if "year" in dict:
        df_copy = pd.merge(df_copy, df_Publication_year, left_on='id_publication', right_on='id_publication',how='inner')
        df_copy = df_copy.loc[df_copy.id_year == 'id_' + dict["year"]]
        source = "id_year"

    graphe(df_copy.head(500), source, 'id_venue')
    return df_copy


def More_info(dict):
    if "author" in dict:
        return (df_author.loc[df_author.id_author==get_id_author(dict['author'])])
    if "publication" in dict:
        return (df_publication.loc[df_publication.id_publication == get_id_pub(dict["publication"])])
    if "venue" in dict:
        return (df_venue.loc[df_venue.id_venue.isin(get_id_venue(dict["venue"]))])
    if "keyword" in dict:
        return (df_keyword.loc[df_keyword.keyword.isin(dict["keyword"].split(","))])
    if "year" in dict:
        return (df_year.loc[df_year.id_year == 'id_' + dict["year"]])

def Info_node(ask,name):
    if ask == "id_author" :
        res=df_author.loc[df_author.id_author==name]
        res= res.to_dict()
        id = str(list(res["id_author"].values()))[1:-1]
        namea = str(list(res["name_author"].values()))[1:-1]
        nbr = str(list(res["nbr_publication"].values()))[1:-1]
        stttr = "id_author : " + id.replace("'","") + "<br>Name author : " + namea.replace("'","") + "<br>Nombre de publication : " + nbr
        return stttr , namea.replace("'","")
    if ask == "id_publication":
        res = df_publication.loc[df_publication.id_publication == name]
        res = res.to_dict()
        id_p = str(list(res["id_publication"].values()))[1:-1]
        d_p = str(list(res["date_pub"].values()))[1:-1]
        n_a = str(list(res["nbr_authors"].values()))[1:-1]
        a_t = str(list(res["article_title"].values()))[1:-1]
        cat = str(list(res["categorie"].values()))[1:-1]
        a_t = a_t.replace("'", "")
        shorter = a_t[:50] + (a_t[50:] and '..')
        stttr = "id publication : " + id_p.replace("'","") + "<br>Date de Publication : " + d_p.replace("'","") + "<br>Nombre des auteurs : " + n_a +"<br>Titre de l'article : " + a_t + "<br>Categorie : "+ cat.replace("'","")

        return stttr , shorter
    if ask == "id_venue":
        res = df_venue.loc[df_venue.id_venue == name]
        res = res.to_dict()
        id_v = str(list(res["id_venue"].values()))[1:-1]
        n_v = str(list(res["name_venue"].values()))[1:-1]
        t_v = str(list(res["type_venue"].values()))[1:-1]
        stttr ="id venue : " + id_v.replace("'","") + "<br>Name venue : " + n_v.replace("'","") + "<br>Type venue : " + t_v.replace("'","")
        return stttr , n_v.replace("'","")
    if ask == "keyword":
        res = df_keyword.loc[df_keyword.keyword == name]
        res = res.to_dict()
        keyword = str(list(res["keyword"].values()))[1:-1]
        n_u = str(list(res["nbr_used"].values()))[1:-1]
        stttr ="Keyword : " + keyword.replace("'","") + "<br>Nombre utilisé : " + n_u
        return stttr , keyword.replace("'","")
    if ask == "id_year":
        res = df_year.loc[df_year.id_year == name]
        res = res.to_dict()
        id_y = str(list(res["id_year"].values()))[1:-1]
        year = str(list(res["year"].values()))[1:-1]
        stttr = "Id Year : " + id_y.replace("'","") + "<br>Year : " + year
        return stttr , year


#------------------ INTERFACE--------------------------
from flask import Flask, render_template, request
import pandas as pd
app = Flask(__name__)





@app.route('/')
def home_page():
   return render_template('dblp_Projet.html')


def getinputs():
    dict = {}
    if request.form.get('tauthor')!="" :
        dict.update({'author': request.form.get('tauthor')})

    if request.form.get('tpublication')!="" :
        dict.update({'publication': request.form.get('tpublication')})

    if request.form.get('tvenue')!="" :
        dict.update({'venue': request.form.get('tvenue')})

    if request.form.get('tkeyword')!="" :
        dict.update({'keyword': request.form.get('tkeyword')})

    if request.form.get('tyear')!="" :
        dict.update({'year': request.form.get('tyear')})

    return dict

      
        

@app.route('/submit', methods=['GET', 'POST'])
def submit():



    if request.form.get('author'):
       df=Author(getinputs())
       df=df.head(20)

       return render_template('requetes.html',  tables=[df.to_html(classes='data', header="true")], iframe = 'static/graphe.html')
   
    elif request.form.get('publication'):
       df=Publication(getinputs())
       df=df.head(20)

       return render_template('requetes.html',  tables=[df.to_html(classes='data', header="true")], iframe = 'static/graphe.html')

   
    elif request.form.get('venue'): 
       df=Venue(getinputs())
       df=df.head(20)

       return render_template('requetes.html',  tables=[df.to_html(classes='data', header="true")], iframe = 'static/graphe.html')

   
    elif request.form.get('keyword'):
       df=Keywords(getinputs())
       df=df.head(20)

       return render_template('requetes.html',  tables=[df.to_html(classes='data', header="true")], iframe = 'static/graphe.html')

    return render_template('dblp_Projet.html')


app.run(debug=True)





