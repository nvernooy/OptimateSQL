/*
	@license Angular Treeview version 0.1.6
	ⓒ 2013 AHN JAE-HA http://github.com/eu81273/angular.treeview
	License: MIT


	[TREE attribute]
	angular-treeview: the treeview directive
	tree-id : each tree's unique id.
	tree-model : the tree model on $scope.
	node-id : each node's id
	node-label : each node's label
	node-children: each node's children

	<div
		data-angular-treeview="true"
		data-tree-id="tree"
		data-tree-model="roleList"
		data-node-id="roleId"
		data-node-label="roleName"
		data-node-children="children" >
	</div>
*/

// Angular Treeview template and render
(function ( angular )
{
    'use strict';
    angular.module( 'angularTreeview', [] ).directive( 'treeModel',
        [
            '$compile',
            function( $compile )
                {
                return {
                    restrict: 'A',
                    link: function ( scope, element, attrs )
                    {
                        //tree id
                        var treeId = attrs.treeId;
                        //tree model
                        var treeModel = attrs.treeModel;
                        //node id
                        var nodeId = attrs.nodeId || 'id';
                        //node label
                        var nodeLabel = attrs.nodeLabel || 'label';
                        //children
                        var nodeChildren = attrs.nodeChildren || 'children';
                        //description
                        var nodeDescription = attrs.nodeDescription || 'description';
                        //tree template
                        var template =
                    	'<ul>' +
                    	    '<li data-ng-repeat="node in ' + treeModel + '">' +
                    	        '<i class="collapsed" data-ng-show="node.' + nodeChildren + '.length && node.collapsed" data-ng-click="' + treeId + '.selectNodeHead(node)"></i>' +
                    	        '<i class="expanded" data-ng-show="node.' + nodeChildren + '.length && !node.collapsed" data-ng-click="' + treeId + '.selectNodeHead(node)"></i>' +
                    	        '<i class="normal" data-ng-hide="node.' + nodeChildren + '.length"></i> ' +
                    	        '<span data-ng-class="node.selected" data-ng-click="' +
                    	            treeId + '.selectNodeLabel(node)">{{node.' + nodeLabel +
                    	            '}}</span>' +
                    	        '<div data-ng-hide="node.collapsed" data-tree-id="' +
                    	            treeId + '" data-tree-model="node.' + nodeChildren +
                    	            '" data-node-id=' + nodeId + ' data-node-label=' +
                    	            nodeLabel + ' data-node-children=' + nodeChildren + '></div>' +
                    	    '</li>' +
                    	'</ul>';


                        //check tree id, tree model
                        if( treeId && treeModel )
                        {
                            //root node
                            if( attrs.angularTreeview )
                            {
                                //create tree object if not exists
                                scope[treeId] = scope[treeId] || {};
                                //if node head clicks,
                                scope[treeId].selectNodeHead =
                                    scope[treeId].selectNodeHead ||
                                    function( selectedNode )
                                    {
                                    //Collapse or Expand
                                    selectedNode.collapsed = !selectedNode.collapsed;
                                    };

                                //if node label clicks,
                                scope[treeId].selectNodeLabel =
                                    scope[treeId].selectNodeLabel ||
                                    function( selectedNode )
                                    {
                                         console.log ("label clicked");
                                        //remove highlight from previous node
                                        if (scope[treeId].currentNode && scope[treeId].currentNode.selected )
                                        {
                                        scope[treeId].currentNode.selected = undefined;
                                        }

                                        //set highlight to selected node
                                        selectedNode.selected = 'selected';

                                        //set currentNode
                                        scope[treeId].currentNode = selectedNode;

                                        // Get children of selected node
                                        // Request to server with ID in header
                                        var response;

                                        var xmlhttp = new XMLHttpRequest();
                                        var url = "http://127.0.0.1:8080/projects";
                                        console.log (url);
                                        xmlhttp.onreadystatechange = function() {
                                            if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
                                                var myArr = JSON.parse(xmlhttp.responseText);
                                                console.log(myArr);
                                                }
                                        }

                                        xmlhttp.open("GET", url, true);
                                        xmlhttp.setRequestHeader("id", scope[treeId].currentNode.ID);
                                        xmlhttp.send();



                                        /*var children = angular.module('getChildren', []);
                                        children.controller('childrenControl',
                                        [
                                            '$scope', '$http', function($scope, $http)
                                            {
                                                $http.get('http://127.0.0.1:8080/project_data',
                                                {
                                                    headers: {'ProjectID': scope[treeId].currentNode.ID}
                                                }).success
                                                (function(data)
                                                     {
                                                        response = data;
                                                     //scope[treeId].currentNode.Subitem = data;
                                                    }

                                                );
                                        }]);*/
                                        console.log(response);
                                        console.log(scope);


                                    };
                            }
                            //Rendering template.
                            //element.html('').append( $compile( template )( scope ) );
                             selectedNode.html('').append( $compile( template )( scope[treeId] ) );
                        }
                    }
                };
            }]);
})( angular );
