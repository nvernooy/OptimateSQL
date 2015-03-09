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
// -----------------------------------------------------------
// Modal dialog module
// The Modal dialog is used for user interaction with the items in Optimate
// It opens a dialog menu with options to select
(function() {
  var app;

  app = angular.module("ngModal", []);

  app.provider("ngModalDefaults", function() {
    return {
      options: {
        closeButtonHtml: "<span class='ng-modal-close-x'>X</span>"
      },
      $get: function() {
        return this.options;
      },
      set: function(keyOrHash, value) {
        var k, v, _results;
        if (typeof keyOrHash === 'object') {
          _results = [];
          for (k in keyOrHash) {
            v = keyOrHash[k];
            _results.push(this.options[k] = v);
          }
          return _results;
        } else {
          return this.options[keyOrHash] = value;
        }
      }
    };
  });

  app.directive('modalDialog', [
    'ngModalDefaults', '$sce', function(ngModalDefaults, $sce) {
      return {
        restrict: 'E',
        scope: {
          show: '=',
          dialogTitle: '@',
          onClose: '&?'
        },
        replace: true,
        transclude: true,
        link: function(scope, element, attrs) {
          var setupCloseButton, setupStyle;
          setupCloseButton = function() {
            return scope.closeButtonHtml =
                        $sce.trustAsHtml(ngModalDefaults.closeButtonHtml);
          };
          setupStyle = function() {
            scope.dialogStyle = {};
            if (attrs.width) {
              scope.dialogStyle['width'] = attrs.width;
            }
            if (attrs.height) {
              return scope.dialogStyle['height'] = attrs.height;
            }
          };
          scope.hideModal = function() {
            return scope.show = false;
          };
          scope.$watch('show', function(newVal, oldVal) {
            if (newVal && !oldVal) {
              document.getElementsByTagName("body")[0].style.overflow = "hidden";
            } else {
              document.getElementsByTagName("body")[0].style.overflow = "";
            }
            if ((!newVal && oldVal) && (scope.onClose != null)) {
              return scope.onClose();
            }
          });
          setupCloseButton();
          return setupStyle();
        },
        template: "<div class='ng-modal' ng-show='show'>\n  "+
                        "<div class='ng-modal-overlay' "+
                            "ng-click='hideModal()'>"+
                        "</div>\n  "+
                        "<div class='ng-modal-dialog' "+
                            "ng-style='dialogStyle'>\n"+
                            "<span class='ng-modal-title' "+
                                "ng-show='dialogTitle && dialogTitle.length' "+
                                "ng-bind='dialogTitle'>"+
                            "</span>\n"+
                            "<div class='ng-modal-close' "+
                                "ng-click='hideModal()'>\n"+
                                "<div ng-bind-html='closeButtonHtml'></div>\n"+
                            "</div>\n"+
                            "<div class='ng-modal-dialog-content'"+
                                "ng-transclude>"+
                            "</div>\n"+
                        "</div>\n"+
                    "</div>"
      };
    }
  ]);

}).call(this);

//------------------------------------------------------------------
// Treeview module
// The Treeview is what is used to display the Optimate objects in a tree-hierarchy
(function ( angular ) {
    'use strict';

    angular.module( 'angularTreeview', ['ngModal'] )
    .directive(
        'treeModel', ['$compile', '$http', function( $compile, $http) {
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
                    // path
                    var nodePath = attrs.nodePath || 'path'
                    // Copied node to be pasted
                    scope.copiednode;
                    // modal shown and other modal variables
                    scope.showoptions = false;
                    scope.showinput = false;
                    scope.showcosts = false

                    //tree template
                    // this is appended to the html and compiled,
                    // the result is seen by the user
                    var template =
                        // iterate through a list adding the items
                        // how they are displayed depends on their current state
                        '<ul>' +
                            '<li data-ng-repeat="node in ' + treeModel + '">' +
                                '<i class="collapsed" ' +
                                    'data-ng-show="node.' + nodeChildren +
                                    '.length && node.collapsed" '+
                                    'data-ng-click="' +
                                    treeId + '.selectNodeHead(node)">'+
                                '</i>' +
                                '<i class="expanded" '+
                                    'data-ng-show="node.' + nodeChildren +
                                    '.length && !node.collapsed" '+
                                    'data-ng-click="' +
                                    treeId + '.selectNodeHead(node)">'+
                                '</i>' +
                                '<i class="normal" '+
                                    'data-ng-hide="node.' + nodeChildren +
                                    '.length">'+
                                '</i> ' +

                                // when a node label is selected a function
                                // based on the node id is called
                                '<span data-ng-class="node.selected" '+
                                    'data-ng-click="' + treeId +
                                    '.selectNodeLabel(node)">'+
                                    '{{node.' + nodeLabel + '}}'+
                                '</span>' +

                                // Modal dialogue with functions
                                // The button to open the options menus is a '+'
                                // that appears when the node is selected
                                '<span class="additem" data-ng-show="node.selected">'+
                                    '<button data-ng-click="showoptions = true;">+</button>'+
                                    '<modal-dialog  show=showoptions '+
                                                    'dialog-title="Options" '+
                                                    'width="150px">'+
                                            // When Add button is pressed
                                            // another modal dialog opens
                                            // with input boxes for the new item
                                            '<button data-ng-click="showinput=true">Add</button>'+
                                                '<modal-dialog show=showinput '+
                                                            'dialog-title="Enter data" '+
                                                            'width="300px">'+
                                                '<form data-ng-submit="'+
                                                            treeId + '.addItem(node.Path)">'+
                                                    'Name:<br>'+
                                                    '<input type="text" '+
                                                            'name="inputName" '+
                                                            'data-ng-model="formData.inputName" '+
                                                            'required '+
                                                            'autofocus>'+
                                                    '<br>Description:<br>'+
                                                    '<input type="text" '+
                                                            'name="inputDescription" '+
                                                            'data-ng-model="formData.inputDescription" '+
                                                            'required '+
                                                            'autofocus>'+
                                                    '<br>Type:<br>'+
                                                    '<input type="radio" '+
                                                            'data-ng-model="formData.inputType" '+
                                                            'data-ng-click="showcosts=false"'+
                                                            'value="project">'+
                                                            'Project<br>'+
                                                    '<input type="radio" '+
                                                            'data-ng-model="formData.inputType" '+
                                                            'data-ng-click="showcosts=false"'+
                                                            'value="budgetgroup">'+
                                                            'BudgetGroup<br>'+
                                                    '<input type="radio" '+
                                                            'data-ng-model="formData.inputType" '+
                                                            'data-ng-click="showcosts=true"'+
                                                            'value="budgetitem">'+
                                                            'BudgetItem<br>'+
                                                    '<div data-ng-show="showcosts">'+
                                                            '<br>Quantity:<br>'+
                                                                '<input type="integer" '+
                                                                'name="inputQuantity" '+
                                                                'data-ng-model="formData.inputQuantity">'+
                                                            '<br>Rate:<br>'+
                                                                '<input type="integer" '+
                                                                'name="inputRate" '+
                                                                'data-ng-model="formData.inputRate">'+
                                                    '</div>'+
                                                    '<input type="submit" '+
                                                        'value="Add"/>'+
                                                    '</form>'+
                                                '</modal-dialog>'+
                                            // Delete an item
                                            '<button data-ng-click='+
                                                        '"' + treeId + '.deleteItem(node.Path, node.ID)">'+
                                                        'Delete'+
                                            '</button>'+
                                            // Copy the path of the item
                                            '<button data-ng-click='+
                                                        '"' + treeId + '.copy(node.Path)">'+
                                                        'Copy'+
                                            '</button>'+
                                            // Paste the item
                                            '<button data-ng-click='+
                                                        '"' + treeId + '.paste(node.Path)">'+
                                                        'Paste'+
                                            '</button>'+
                                            // Get the cost of the item
                                            '<button data-ng-click='+
                                                        '"' + treeId + '.costItem(node.Path)">'+
                                                        'Get total cost'+
                                            '</button>'+
                                    '</modal-dialog>'+
                                '</span>'+

                                '<div data-ng-hide="node.collapsed" '+
                                    'data-tree-id="' + treeId +
                                    '" data-tree-model="node.' + nodeChildren +
                                    '" data-node-id=' + nodeId +
                                    ' data-node-label=' + nodeLabel +
                                    ' data-node-children=' + nodeChildren + '>'+
                                    ' data-node-path=' + nodePath + '>'+
                                '</div>' +
                            '</li>' +
                        '</ul>';


                    //check tree id, tree model
                    if( treeId && treeModel ) {
                        //root node
                        if( attrs.angularTreeview ) {
                            //create tree object if not exists
                            scope[treeId] = scope[treeId] || {};

                            // function to add item to Optimate
                            scope[treeId].addItem = function(path) {
                                // Get values from the user input
                                // and clear the input forms
                                var name = scope.formData.inputName;
                                scope.formData.inputName = "";
                                var description = scope.formData.inputDescription;
                                scope.formData.inputDescription = "";
                                var type = scope.formData.inputType;
                                var quantity = scope.formData.inputQuantity;
                                scope.formData.inputQuantity=0
                                var rate = scope.formData.inputRate;
                                scope.formData.inputRate=0

                                console.log("Adding a " + type + " " + name +
                                    ", " + description + " to: " +path);

                                // the item is found by routing to it's path
                                // and adding the function to be executed
                                $http({
                                    method: 'POST',
                                    url: 'http://localhost:8100' + path + 'add',
                                    data:{  'Name': name,
                                            'Description':description,
                                            'Type': type,
                                            'Quantity': quantity,
                                            'Rate': rate}
                                }).success(
                                    function () {
                                        alert('Success: Child added');
                                        console.log("added");
                                    }
                                );
                            }

                            // Function to delete data in server
                            scope[treeId].deleteItem = function(path) {
                                console.log("Deleting "+ path);
                                $http({
                                    method: 'POST',
                                    url:'http://localhost:8100'+path+'delete'
                                }).success(
                                        function () {
                                            alert('Success: Item deleted');
                                        }
                                    );
                            }

                            // Function to copy a node
                            // the node address only is copied into the scope
                            scope[treeId].copy = function(cnode) {
                                scope.copiednode = cnode;
                                console.log("Path that is copied: " +
                                            scope.copiednode);
                                alert('Node address copied')
                            }

                            // function to POST data to server to paste item
                            scope[treeId].paste = function(path) {
                                console.log("Node to be pasted: " +
                                            scope.copiednode);
                                $http({
                                    method: 'POST',
                                    url: 'http://localhost:8100' + path + 'paste',
                                    data:{'Path': scope.copiednode}
                                }).success(
                                    function () {
                                        alert('Success: Node pasted');
                                    }
                                );
                            }

                            // Function to get the cost of the node
                            scope[treeId].costItem = function(path) {
                                console.log("Costing "+ path);
                                $http.get('http://127.0.0.1:8100'+path+'cost').success
                                    (
                                    function(data)
                                        {
                                            console.log("Htpp request success: "+ data);
                                             // get the cost of the node and post alert
                                            alert(data['Cost']);
                                        }
                                    );
                            }

                            //if node head clicks,
                            scope[treeId].selectNodeHead =
                            scope[treeId].selectNodeHead ||
                            function( selectedNode ){
                                //Collapse or Expand
                                selectedNode.collapsed = !selectedNode.collapsed;
                            };

                            //if node label clicks,
                            scope[treeId].selectNodeLabel =
                            scope[treeId].selectNodeLabel ||
                            function( selectedNode ){
                                //remove highlight from previous node
                                if( scope[treeId].currentNode &&
                                    scope[treeId].currentNode.selected ) {
                                    scope[treeId].currentNode.selected = undefined;
                                }

                                //set highlight to selected node
                                selectedNode.selected = 'selected';

                                //set currentNode
                                scope[treeId].currentNode = selectedNode;

                                // get path from the node
                                // and go to that path with http
                                var path = scope[treeId].currentNode.Path;
                                console.log(path);
                                $http.get('http://127.0.0.1:8100'+path).success
                                    (
                                    function(data)
                                        {
                                            console.log("Htpp request success: "+ data);
                                             // Append the response data to the
                                             // subitem (children) of the
                                             // current node
                                            scope[treeId].currentNode.Subitem =  data;
                                        }
                                    );
                            };
                        }
                        //Rendering template.
                        element.html('').append( $compile( template )( scope ) );
                    }
                }
            };
    }]);
})( angular );
