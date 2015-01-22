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

(function ( angular ) {
    'use strict';

    angular.module( 'angularTreeview', [] ).directive( 'treeModel', ['$compile', function( $compile ) {
        return {
            restrict: 'A',
            link: function ( scope, element, attrs ) {
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

                //tree template
                var template =
                    '<ul>' +
                        '<li data-ng-repeat="node in ' + treeModel + '">' +
                            '<i class="collapsed" data-ng-show="node.' + nodeChildren + '.length && node.collapsed" data-ng-click="' + treeId + '.selectNodeHead(node)"></i>' +
                            '<i class="expanded" data-ng-show="node.' + nodeChildren + '.length && !node.collapsed" data-ng-click="' + treeId + '.selectNodeHead(node)"></i>' +
                            '<i class="normal" data-ng-hide="node.' + nodeChildren + '.length"></i> ' +
                            '<span data-ng-class="node.selected" data-ng-click="' + treeId + '.selectNodeLabel(node)">{{node.' + nodeLabel + '}}</span>' +
                            '<div data-ng-hide="node.collapsed" data-tree-id="' + treeId + '" data-tree-model="node.' + nodeChildren + '" data-node-id=' + nodeId + ' data-node-label=' + nodeLabel + ' data-node-children=' + nodeChildren + '></div>' +
                        '</li>' +
                    '</ul>';


                //check tree id, tree model
                if( treeId && treeModel ) {

                    //root node
                    if( attrs.angularTreeview ) {

                        //create tree object if not exists
                        scope[treeId] = scope[treeId] || {};

                        //if node head clicks,
                        scope[treeId].selectNodeHead = scope[treeId].selectNodeHead || function( selectedNode ){

                            //Collapse or Expand
                            selectedNode.collapsed = !selectedNode.collapsed;
                        };

                        //if node label clicks,
                        scope[treeId].selectNodeLabel = scope[treeId].selectNodeLabel || function( selectedNode ){

                            //remove highlight from previous node
                            if( scope[treeId].currentNode && scope[treeId].currentNode.selected ) {
                                scope[treeId].currentNode.selected = undefined;
                            }

                            //set highlight to selected node
                            selectedNode.selected = 'selected';
                            console.log("Node clicked");

                            //set currentNode
                            scope[treeId].currentNode = selectedNode;
                            // get path from parentid in node
                            // and go to that path with http
                            // console.log ("Sending http request");
                            // http.get('http://127.0.0.1:8080'+'/1').success
                            // (
                            //     function(data)
                            //         {
                            //             scope.roleList = data;
                            //         }
                            // );
                            // console.log("Htpp request success: "+scope.roleList);
                            var xmlhttp = new XMLHttpRequest();

                            var path = "";
                            // Get path
                            if (scope[treeId].currentNode.Parent == "0"){
                                path = scope[treeId].currentNode.ID;
                            }
                            else{
                                path =  scope[treeId].currentNode.Parent + "/" + scope[treeId].currentNode.ID;
                            }

                            console.log(path);
                            var url = "http://127.0.0.1:8080/"+path;
                            var response;
                            xmlhttp.onreadystatechange = function() {
                                if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
                                    response = JSON.parse(xmlhttp.responseText);

                                    // for (var key in response[0]){
                                    //     console.log(key + ": " + response[0][key] );
                                    // }

                                    console.log(scope[treeId].currentNode);
                                    scope[treeId].currentNode.Subitem = response;
                                    console.log(scope[treeId].currentNode.Subitem);
                                    console.log(scope[treeId].currentNode);
                                    // //Rendering template again.
                                    // element.html('').append( $compile( template )( scope ) );
                                }
                            };
                            +
                            xmlhttp.open("GET", url, true);
                            xmlhttp.send();
                             // console.log(response);
                            // scope[treeId] = response;

                        };
                    }

                    //Rendering template.
                    element.html('').append( $compile( template )( scope ) );

                    console.log("rendering complete");
                    console.log(scope[treeId]);
                }
                else{
                console.log("Treeid not treemodel");
            }
            }
        };
    }]);
})( angular );
