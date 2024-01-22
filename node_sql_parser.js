<!DOCTYPE html>
<html>
<head>
	<title>node-sql-parser</title>

	<!-- Node Sql Parser -->
  <script src="https://unpkg.com/node-sql-parser/umd/mysql.umd.js"></script>
  
  <script>
    window.onload = function () {
      console.log('window.onload');
    }
  </script>
  
  <!-- Graph MX - Sets the basepath for the library if not in same directory -->
	<script type="text/javascript">
		mxBasePath = '../src';
	</script>

	<!-- Graph MX - Loads and initializes the library -->
	<script type="text/javascript" src="../src/js/mxClient.js"></script>
  
	<!-- Example code -->
	<script type="text/javascript">
    
    // Parse SQL
    function parseSql(p_sql) {
      // Example parser
      const parser = new NodeSQLParser.Parser();
      const ast = parser.astify(p_sql);
      return ast;
    };
    
    function astToSql(p_ast) {
      const parser = new NodeSQLParser.Parser();
      const sql = parser.sqlify(p_ast);
      return sql;
    };
    
    function getAst() {
      var sql = document.getElementById("sqlInput").value;
      var ast = parseSql(sql);
      return ast;
    };
    
    function fn_btnParse() {
      //"select id, name from students where age < 18"
      var ast = getAst();
      
      var astJson = JSON.stringify(ast, null, 2);
      astOutput.value = astJson;
    };
    
    // Copy parsed SQL Ast to clipboard
    function copyAstOutput() {
      // Get the text field
      var copyText = document.getElementById("astOutput");

      // Select the text field
      copyText.select();
      copyText.setSelectionRange(0, 99999); // For mobile devices

      // Copy the text inside the text field
      navigator.clipboard.writeText(copyText.value);

      // Alert the copied text
      //alert("Copied the text: " + copyText.value);
    };
    
    // Insert sample sql to text area
    function insertSql(p_name) {
    
    console.log(p_name);
      var sql = document.getElementById(p_name).innerText; 
      
      console.log(sql);
      
      document.getElementById("sqlInput").value = sql;
      
    };
    
    function drawAst(graph, parent, node, source, depth) {
      console.log('--- node:');
      console.log(node);
      
      console.log('--- depth:' + depth);
      
      //if (depth > 0) {
      //  console.log('exiting...');
      //  return 0;
      //}
      // http://localhost:8081/mxgraph-master/javascript/examples/node_sql_parser.html
      var ast, a;
      if (node)
        ast = node;
      else
        //ast = getAst();
        ast = null;
      
      if (Array.isArray(ast) && ast.length > 0)
        a = ast[0];
      else
        a = ast;
      
      if (a) {
        var vs, vf;
        //if (a.type == 'select')
        //  vs = graph.insertVertex(parent, null, 'Select!', 300, 150, 80, 30);
        
        if (a.from) {
          vs = graph.insertVertex(parent, null, 'From', 300, 150, 80, 30);
          
          if (source)
            graph.insertEdge(parent, null, '', source, vs);
          
          //
          //if (depth > 0) { console.log('exiting...'); return 0; }
          
          for (var i=0; i<a.from.length; i++) {
            
            var from = a.from[i];
            
            if (from.table) {
              val = a.from[i].table;
              vf = graph.insertVertex(parent, null, val, 300, 150, 80, 30);
              if (vs)
                graph.insertEdge(parent, null, '', vs, vf);
            }
            else if (from.expr) {
              var expr = from.expr;
              val = 'EXPR';
              ve = graph.insertVertex(parent, null, val, 300, 150, 80, 30);
              if (vs)
                graph.insertEdge(parent, null, '', vs, ve);
              if (expr.ast) {
                drawAst(graph, parent, expr.ast, ve, depth+1);
              }
            }
          }
        }
      }
      
      
      //console.log(ast);
    };
    
    // Program starts here. Creates a sample graph in the
		// DOM node with the specified ID. This function is invoked
		// from the onLoad event handler of the document (see below).
		function drawSql()
		{
      var container = document.getElementById('graphContainer');
      container.innerHTML = '';
			// Checks if the browser is supported
			if (!mxClient.isBrowserSupported())
			{
				// Displays an error message if the browser is not supported.
				mxUtils.error('Browser is not supported!', 200, false);
			}
			else
			{
				// Disables the built-in context menu
				mxEvent.disableContextMenu(container);
				
				// Creates the graph inside the given container
				var graph = new mxGraph(container);

				// Enables rubberband selection
				new mxRubberband(graph);
				
				// Gets the default parent for inserting new cells. This
				// is normally the first child of the root (ie. layer 0).
				var parent = graph.getDefaultParent();
        
        var layout = new mxHierarchicalLayout(graph);
        
        var mxGraphButtons = document.getElementById('mxGraphButtons');
        
        mxGraphButtons.innerHTML = '';
        
        // BOTTUN Horizontal layout
				mxGraphButtons.appendChild(mxUtils.button('Horizontal',function(evt)
				{
					var parent = graph.getDefaultParent();
          layout = new mxHierarchicalLayout(graph);
          layout.orientation = mxConstants.DIRECTION_WEST;
					layout.execute(parent);
				}));
        
        // BOTTUN Vertical layout
				mxGraphButtons.appendChild(mxUtils.button('Vertical',function(evt)
				{
					var parent = graph.getDefaultParent();
          layout = new mxHierarchicalLayout(graph);
          layout.orientation = mxConstants.DIRECTION_NORTH;
					layout.execute(parent);
				}));
        
        // Adds a button to execute the layout
				//var button = document.createElement('button');
				//mxUtils.write(button, 'WriteUpdate');
				//mxEvent.addListener(button, 'click', function(evt)
				//{
				//	layout.execute(parent);
				//});
				//document.body.appendChild(button);
								
				// Adds cells to the model in a single step
				graph.getModel().beginUpdate();
				try
				{
					//var v1 = graph.insertVertex(parent, null, 'Hello,', 20, 20, 80, 30);
					//var v2 = graph.insertVertex(parent, null, 'World!', 200, 150, 80, 30);
					//var e1 = graph.insertEdge(parent, null, '', v1, v2);
          
          console.log('Ajmo crtat!');
          
          drawAst(graph, parent, getAst(), null, 0);
          layout.orientation = mxConstants.DIRECTION_WEST;
          layout.execute(parent);
				}
				finally
				{
					// Updates the display
					graph.getModel().endUpdate();
				}
			}
		};
    
	</script>
  
  
  
</head>

<!--
<body onload="main()" style="margin:4px;">
-->

<body style="margin:4px;">

<!-- Input SQL -->
<label for="sqlInput">Insert SQL query or generate: </label>
<button onclick="insertSql('sqlSimple')">Simple SQL</button>
<button onclick="insertSql('sqlSimple1')">Simple SQL1</button>
<button onclick="insertSql('sqlJoin')">SQL with JOIN</button>
<button onclick="insertSql('sqlJoin3')">SQL with 3 JOIN</button>
<br/>
<br/>
<textarea id="sqlInput" name="sqlInput" rows="10" cols="100">
-- sql query
select jedan, dva, tri from tablica_01;
</textarea>
<br/>
<br/>
<button onclick="fn_btnParse()">Parse</button>
<button onclick="drawSql()">Draw</button>
<br/>
<br/>
<hr/>

<!-- Output AST -->
<label for="astOutput">Parsed SQL:</label>
<br/>
<br/>
<textarea id="astOutput" name="astOutput" rows="10" cols="100">
-- AST
</textarea>
<br/>
<br/>
<button onclick="copyAstOutput()">Copy</button>

<hr/>
  <!-- document.getElementById('graphContainer')) -->
  <!-- mxGraph div -->
  <!-- 
<div id="graphContainer" style="position: absolute; overflow: auto; inset: 50px 0px 0px 24px; background: url(&quot;editors/images/grid.gif&quot;); touch-action: none;"></div>
-->
<p id='mxGraphButtons'><p>

<div id="graphContainer" style="position: relative; width:100%;height:100%; overflow: auto; inset: 20px 20px 20px 20px; background: url(&quot;editors/images/grid.gif&quot;); touch-action: none;"></div>

   
<p id="sqlSimple" hidden>select jedan, dva, tri from tablica_01;</p>
  
<p id="sqlSimple1" hidden>select id, name from students where age &lt; 18</p>
  
<p id="sqlJoin" hidden>select col1, col2, col3 from table_01 t1 
left join table_02 t2 on t1.id=t2.id;</p>

<p id="sqlJoin3" hidden>
with tb_w1 as (select * from wi_table)
select col1, col2, col3 
from table_01 t1 
left join table_02 t2 
 on t1.id=t2.id
left join (select * from table_03) t3
  on t3.id=t2.id;</p>

</body>
</html>
