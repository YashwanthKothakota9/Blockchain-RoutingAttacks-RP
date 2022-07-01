from flask import Flask,request,render_template,redirect
from neo4j import GraphDatabase

driver=GraphDatabase.driver(uri="bolt://100.25.170.168:33264",auth=(id,pwd))
session=driver.session()

app=Flask(__name__)
@app.route("/keyword_discovery",methods=["GET","POST"])
def keyword_discovery():
    if request.method=="POST":
        research_topic=request.form["rtopic"]
        limit=request.form["limit"]
        order=request.form["order"]
        query="""MATCH (k:keyword) <-[s:has_research_topic] - (a:Author)
                WHERE k.key = {research_topic:$research_topic}
                WITH k,a,s 
        RETURN k.key,a.name,s.score,s.relevance ORDER BY s.relevance {order:$order}, s.score {order:$order} limit {limit:$limit}"""
        parameter={"research_topic":research_topic,"limit":limit,"order":order}
        results=session.run(query,parameter)
        return render_template("query1_results.html",list=results)
    else:
        return render_template("home.html")


@app.route("/research_profiling",methods=["GET","POST"])
def research_profiling():
    if request.method=="POST":
        author_name=request.form["aname"]
        limit=request.form["limit"]
        order=request.form["order"]
        query="""MATCH (b:Author) - [l:has_research_topic] -> (k:keyword) <- [r:has_research_topic] - (a:Author)

WHERE a.name={author_name:$author_name}

WITH b,k,l.score as sugg_author_score,

    l.relevence as sugg_author_relevence,

    r.score as author_score,

    r.relevence as author_relevence

WITH collect([b,author_relevence,author_score,sugg_author_relevence,

        sugg_author_score]) as researchers_data, k

UNWIND researchers_data[0..3] AS r

WITH k,(r[0]).name as name, r[3] as sugg_author_relevence, r[4] as

    sugg_author_score, r[1] as author_relevence, r[2] as author_score

RETURN k.key as Topic, name, author_score, author_relevence,

    sugg_author_relevence, sugg_author_score ORDER BY sugg_author_relevence {order:$order}, sugg_author_score {order:$order} limit {limit:$limit} """

        parameter={"author_name":author_name,"limit":limit,"order":order}
        results=session.run(query,parameter)
        return render_template("query2_results.html",list=results)
    else:
        return render_template("home.html")



@app.route("/influencing_author",methods=["GET","POST"])
def influencing_author():
    if request.method=="POST":
        research_topic=request.form["rtopic"]
        limit=request.form["limit"]
        order=request.form["order"]
        query="""MATCH (k:keyword) <- [s:has_research_topic] - (a:Author)
WHERE k.key ={research_topic:$research_topic} WITH k,a,s
RETURN a.name,a.pagerank ORDER BY a.pagerank {order:$order} limit {limit:$limit}"""
        parameter={"research_topic":research_topic,"limit":limit,"order":order}
        results=session.run(query,parameter)
        return render_template("query3_results.html",list=results)
    else:
        return render_template("home.html")


app.run(port=5000)