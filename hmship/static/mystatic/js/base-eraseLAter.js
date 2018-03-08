    var mainApp = angular.module('mainAppAngular', ['ui.bootstrap', 'ngMessages']);
                    //APP CONFIGURATION OPTIONS
    mainApp.config(['$httpProvider', '$interpolateProvider', function($httpProvider, $interpolateProvider) {
        $interpolateProvider.startSymbol('[[').endSymbol(']]');
        $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    }]);


mainApp.controller('navBarController', function( $scope, $http, postRequest, $element, $window) {
  //var pepa = location.pathname.split("/")[1];
  
    //$scope.logoSize = function(){
        // $scope.hgt = 1;
        // window.addEventListener("resize", function(){
        //     alert('hola')
        //     var thisScreen = new Screen();
        //     alert('alberto')
        //     $scope.hgt = 20;

        // });

        // $scope.hgt = (0.015) * $scope.screen.width + 14.62;
        // alert($scope.hgt)
        //return String($scope.hgt);
        //get current screen size
    // $scope.heightString = String( $scope.heightLogo ) + 'px';
        // $scope.screen = new Screen();
        // $scope.hgt = String( (0.015) * $scope.screen.width + 14.62 )+'px';
        // $scope.styler =  { 'height': $scope.hgt, 'position': 'relative', 'width':'auto' };

});
  
mainApp.directive("ngFileSelect",function(){    
  return {
    link: function($scope,el){          
      el.bind("change", function(e){          
        $scope.file = (e.srcElement || e.target).files[0];
        $scope.getFile();
      });          
    }        
  }
});

    mainApp.directive('scale', function($window ) {

           var directive = {};
           directive.restrict = 'A';
           //directive.transclude = true;
           directive.scope = false;
           //directive.templateUrl = '/static/directiveTemplates/modalForm1.html';
           directive.link = function(scope, element, attributes) {
                function calculatesize(){
                    var w = window,
                        d = document,
                        e = d.documentElement,
                        g = d.getElementsByTagName('body')[0]
                        height = w.innerHeight|| e.clientHeight|| g.clientHeight;
                        width = w.innerWidth || e.clientWidth || g.clientWidth;
                        element.css('height', String( width * attributes.scale + 14.69 )+ 'px' );  
                }

                calculatesize();

                angular.element($window).bind('resize', function(){
                  calculatesize();
                  scope.$apply();
               });

           };
           return directive;
    });

    mainApp.directive('modalForm', function() {

           var directive = {};
           directive.restrict = 'E';
           directive.transclude = true;
           directive.scope = false;
           directive.templateUrl = '/static/directiveTemplates/modalForm1.html';
           return directive;
    });

    mainApp.directive('logoCondominioaldia', function() {

           var directive = {};
           directive.restrict = 'E';
           directive.scope = {
              scale:'@'
           };
           directive.templateUrl = '/static/directiveTemplates/logo1Vector.html';
           return directive;
    });

    mainApp.directive('amexLogo', function() {

           var directive = {};
           directive.restrict = 'E';
           directive.scope = {
              scale:'@',
              height:'@'
           };
           directive.templateUrl = '/static/directiveTemplates/amexlogo.html';
           return directive;
    });

    mainApp.directive('discoverLogo', function() {

           var directive = {};
           directive.restrict = 'E';
           directive.scope = {
              scale:'@',
              height:'@'
           };
           directive.templateUrl = '/static/directiveTemplates/discoverlogo.html';
           return directive;
    });

    mainApp.directive('visaLogo', function() {

           var directive = {};
           directive.restrict = 'E';
           directive.scope = {
              height:'@',
              width:'@'
           };
           directive.templateUrl = '/static/directiveTemplates/visalogo.html';
           return directive;
    });



    mainApp.directive('mastercardLogo', function() {

           var directive = {};
           directive.restrict = 'E';
           directive.scope = {
              height:'@',
              width:'@'
           };
           directive.templateUrl = '/static/directiveTemplates/mastercardlogo.html';
           return directive;
    });

    mainApp.directive('venezuelaFlag', function() {

       var directive = {};
       directive.restrict = 'E';
       directive.scope = {
          scale:'@',
          height:'@',
          width:'@'
       };
       directive.templateUrl = '/static/directiveTemplates/venezuelaFlag.html';
       return directive;
    });

    mainApp.directive('argentinaFlag', function() {

       var directive = {};
       directive.restrict = 'E';
       directive.scope = {
          scale:'@',
          height:'@',
          width:'@'
       };
       directive.templateUrl = '/static/directiveTemplates/argentinaFlag.html';
       return directive;
    });



    mainApp.directive('juntaCondominioBadge', function() {
        var directive = {};
        directive.restrict = 'E';
        directive.transclude = true;
        directive.scope = false;
        directive.templateUrl = '/static/directiveTemplates/junta_condominio_badge.html';
        return directive; 
     });

    mainApp.directive('modalNoTrigger', function() {

           var directive = {};
           directive.restrict = 'E';
           directive.transclude = true;
           directive.scope = {
              directiveclass:'@class'
           };
           directive.templateUrl = '/static/directiveTemplates/modalFormNoTriggerButton.html';
           //directive.require = 'ngModel';
           directive.link = function(scope, element, attributes, ngModel) {
                //alert(attributes.fade);
                if(attributes.id){
                    element.find('.modal').addClass(attributes.id);
                }
                if(attributes.modalSize){
                    if (attributes.modalSize=='small'){
                        element.find('.sizeOptions').addClass('modal-sm');
                    }else if(attributes.modalSize == 'medium'){
                        element.find('.sizeOptions').addClass('modal-md');
                    }else if(attributes.modalSize=='large'){
                        element.find('.sizeOptions').addClass('modal-lg');
                    }

                }else{
                    return false;
                }
                if(attributes.fade == 'true') {
                    element.find('.modal').addClass('fade');
                    //angular.element('#modal-no-trigger').addClass('fade');
                }else{
                    //angular.element('#modal-no-trigger').removeClass('fade');
                    element.find('.modal').removeClass('fade');
                }
            }

           return directive;
    });



    mainApp.directive("matchHeight", [ '$window'  ,function($window) {
      return {
          restrict: "A",
          scope:{
            otherelement:'@matchHeight'
          },
          //require: "ngModel",
           
          link: function(scope, element, attributes, ngModel) {

                //$window.bind("resize", reheight());

                angular.element($window).bind('resize', function() {
                  scope.onResize();
                })

                scope.onResize = function (){
                  var otherelement =  document.getElementById( scope.otherelement );
                  var height = otherelement.clientHeight;
                  element.css('height', String(height)+'px'); 
                  //scope.$apply();        
                }

                scope.onResize();

              // ngModel.$validators.checkpasswordexist = function(modelValue) { 
              //    if (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(modelValue))  
              //     {  
              //       return (true)  ;
              //     }   
              //       return (false)  ;
              // }
          }
      };
    }]);



    mainApp.directive("checkemailvalidity", function() {
      return {
          restrict: "A",
           
          require: "ngModel",
           
          link: function(scope, element, attributes, ngModel) {
              ngModel.$validators.checkpasswordexist = function(modelValue) { 
                 if (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(modelValue))  
                  {  
                    return (true)  ;
                  }   
                    return (false)  ;
              }
          }
      };
    });

    mainApp.directive("passwordmatch", function() {
        return {
            restrict: "A",
            require: "ngModel",
            scope:{
              passwordmatch : '=',
              directivemodel : '=ngModel'
            },
            link: function(scope, element, attributes, ngModel) {
                ngModel.$validators.passwordmatch = function(modelValue) {
                  return modelValue == scope.passwordmatch;
                }
            }
        };
    });

    mainApp.directive("passwordnomatch", function() {
        return {
            restrict: "A",
            require: "ngModel",
            scope:{
              passwordnomatch : '=',
              directivemodel : '=ngModel'
            },
            link: function(scope, element, attributes, ngModel) {
                ngModel.$validators.passwordnomatch = function(modelValue) {
                  return modelValue != scope.passwordnomatch;
                }
            }
        };
    });


    // mainApp.directive("timeDiff", function($interval) {
    //     var directive = {};
    //     directive.restrict = 'E';
    //     directive.transclude = false;
    //     directive.scope = {
    //         startdate:'=',
    //         stringtodate:'&',
    //         enddate: '@'
    //     };
    //     //directive.require = '?ngModel';
    //     directive.templateUrl = '/static/directiveTemplates/date-diff.html';
    //     directive.link = function( scope, element, attributes, ngModel ) {
    //         scope.endate= stringtodate(scope.enddate)
    //         alert(scope.endate)
    //         var updateTime = function() {
    //             var delta =  (scope.endate - scope.startdate)/1000;

    //             // calculate (and subtract) whole days
    //             var days = Math.floor(delta / 86400);
    //             delta -= days * 86400;

    //             // calculate (and subtract) whole hours
    //             var hours = Math.floor(delta / 3600) % 24;
    //             delta -= hours * 3600;

    //             // calculate (and subtract) whole minutes
    //             var minutes = Math.floor(delta / 60) % 60;
    //             delta -= minutes * 60;

    //             // what's left is seconds
    //             var seconds = delta % 60;  // in theory the modulus is not required

    //             if( scope.startdate > scope.endate ){
    //                 scope.difference = 'CERRADA';
    //             }else{
    //                 if (days > 1){
    //                     scope.difference = String(days) + ' dias ' +  String(hours) + ' horas ';
    //                 }else if(days == 1){
    //                     scope.difference = String(days) + ' dia ' +  String(hours) + ' horas ';
    //                 }else if( days < 1){
    //                     scope.difference = String(hours) + ' horas ' + String(minutes) + ' minutos ' + String(seconds.toFixed(0)) + ' s';
    //                 }else if(hours == 1){
    //                     scope.difference = String(hours) + ' hora ' +  String(minutes) + ' minutos ' + String(seconds.toFixed(0)) + ' s';
    //                 }else if( hours < 1){
    //                     scope.difference = String(minutes) + ' minutos ';
    //                 }else if( minutes == 1){
    //                     scope.difference = String(minutes) + ' minuto ';
    //                 }
    //             }
    //         };
  
    //         //schedule update every second
    //         var timer = $interval(updateTime, 1000);
      
    //         // listen on DOM destroy (removal) event, and cancel the next UI update
    //         // to prevent updating time after the DOM element was removed.
    //         element.bind('$destroy', function() {
    //             $interval.cancel(timer);
    //         });
    //     };
    //     return directive;
    // });

    mainApp.directive("dateInputWidget", function() {
        var directive = {};
        directive.restrict = 'E';
        directive.transclude = false;
        directive.scope = true;
        directive.require = 'ngModel';
        directive.templateUrl = '/static/directiveTemplates/date-input-widget.html';
        directive.link = function( scope, element, attributes, ngModel ) {
            var validateDate = function (){
                if (attributes.required){
                    if ( !scope.years || !scope.months || !scope.dias ){
                        ngModel.$setViewValue(null);
                    }else{
                        var selectedDate = new Date(scope.years, scope.months-1, scope.dias)
                        ngModel.$setViewValue(selectedDate);
                    }
                    ngModel.$setTouched();
                }else{
                    ngModel.$validators.required = function(modelValue){
                        return true;
                    }
                }
            }       
            scope.yearList  = [];
            scope.monthList = [
                { 'name': 'Enero', 'value' : 1 }, 
                { 'name': 'Febrero', 'value' : 2 },
                { 'name': 'Marzo', 'value' : 3 },
                { 'name': 'Abril', 'value' : 4 },
                { 'name': 'Mayo', 'value' : 5 },
                { 'name': 'Junio', 'value' : 6 },
                { 'name': 'Julio', 'value' : 7 },
                { 'name': 'Agosto', 'value' : 8 },
                { 'name': 'Septiembre', 'value' : 9 },
                { 'name': 'Octubre', 'value' : 10 },
                { 'name': 'Noviembre', 'value' : 11},
                { 'name': 'Diciembre', 'value' : 12 }
            ];
            scope.dayList = [];

            if(attributes.minDate){
                var minDate = new Date( attributes.minDate );
            }else{
                var minDate = new Date();
                minDate.setFullYear(minDate.getUTCFullYear() - 10);
            }

            if(attributes.maxDate){
                var maxDate = new Date( attributes.maxDate );
            }else{
                var maxDate = new Date();
                maxDate.setFullYear(maxDate.getUTCFullYear() + 10);
            }

            var year_range = {
                'min': minDate.getUTCFullYear(),
                'max': maxDate.getUTCFullYear()
            }

            //FILL YEAR LIST
            for ( var i = year_range.min; i <= year_range.max; i++){
                scope.yearList.push(i);
            }

            element.find('select[ name = "years" ]').on( 'change', function (){
                //////////////////////////////
                scope.dias = '';
                if( scope.years ){
                    scope.monthList = [];
                }
                /////////////////////////////////
                if ( scope.years && scope.months){
                    scope.dayList = [];
                    var last_day_of_month = new Date( scope.years, scope.months, 0).getDate();
                    for (var i = 1; i <= last_day_of_month ; i++){
                        scope.dayList.push(i);
                    }
                }
                validateDate();
                scope.$apply(); //this triggers a $digest
            });

            element.find('select[ name = "months"]').on( 'change', function (){
                scope.dias = '';
                if ( scope.years && scope.months){
                    scope.dayList = [];
                    var last_day_of_month = new Date( scope.years, scope.months, 0).getDate();
                    for (var i = 1; i <= last_day_of_month ; i++){
                        scope.dayList.push(i);
                    }
                }
                validateDate();
                scope.$apply(); //this triggers a $digest
            });

            element.find('select[ name = "dias"]').on( 'change', function (){
                validateDate();
                scope.$apply(); //this triggers a $digest
            });
            }
        return directive;
    });



mainApp.directive("yearMonthDateInput", function() {
     var directive = {};
     directive.restrict = 'E';
     directive.transclude = true;
     directive.scope = {
        name:'@',
        directivemodel : '=ngModel',
        mindate:'@', // YYYY/MM/DD(string)
        maxdate:'@',
        required:'@'  // YYYY/MM/DD(string)
     };
     directive.require = '?ngModel';
     directive.templateUrl = '/static/directiveTemplates/yearmonthdateinput.html';
     directive.link = function(scope, element, attributes, ngModel) {

        if (!attributes.mindate){
            scope.mindate = new Date();
        }
        if (!attributes.maxdate){
            var now = new Date();
            scope.maxdate = now.addDays(5000);
        }
        scope.monthList = [
            { 'name': 'Enero', 'value' : 1 }, 
            { 'name': 'Febrero', 'value' : 2 },
            { 'name': 'Marzo', 'value' : 3 },
            { 'name': 'Abril', 'value' : 4 },
            { 'name': 'Mayo', 'value' : 5 },
            { 'name': 'Junio', 'value' : 6 },
            { 'name': 'Julio', 'value' : 7 },
            { 'name': 'Agosto', 'value' : 8 },
            { 'name': 'Septiembre', 'value' : 9 },
            { 'name': 'Octubre', 'value' : 10 },
            { 'name': 'Noviembre', 'value' : 11},
            { 'name': 'Diciembre', 'value' : 12 }
        ];

        //get year range
        scope.yearList = yearRange(scope.mindate, scope.maxdate);
        function yearRange(mindate, maxdate){
          var yearList = [];
          for (var i = mindate.getUTCFullYear(); i<=maxdate.getUTCFullYear(); i++){
            yearList.push(i);
          }
          return yearList;
        }

        scope.selectorsChange = function(source){
          if ( source == 'year' ){
            scope.month ='';
            scope.directivemodel = '';
          }
          if (scope.year && scope.month){
            scope.directivemodel = new Date(String(scope.year), scope.month-1, 1).toISODate();
          }else{
            scope.directivemodel = '';
          } 

        }

        scope.setnullification = function(year, month){
          if (scope.year){
            var selection_date = new Date(year, month-1, 1);
            if(selection_date !='Invalid Date' && selection_date && (selection_date > scope.maxdate || selection_date <= scope.mindate)){
              return  true; 
            }else if (selection_date =='Invalid Date'){
              return  false;
            }          
          }else{
            return false;
          }

        }

     };
     return directive;
});


// mainApp.directive("myAngularTable", function() {
//      var directive = {};
//      directive.restrict = 'E';
//      directive.transclude = true;
//      directive.scope = false;
//      directive.require = '?ngModel';
//      directive.templateUrl = '/static/directiveTemplates/angularTable.html';
//      directive.link = function(scope, element, attributes, ngModel) {};
//      return directive;
// });


    mainApp.directive("dateSelector", function() {

           var directive = {};
           directive.restrict = 'E';
           directive.transclude = true;
           directive.scope = {
              minDate : '=',
              maxDate : '='
           };
           directive.require = 'ngModel';
           directive.templateUrl = '/static/directiveTemplates/date-picker.html';
           directive.link = function(scope, element, attributes, ngModel) {
            function dateInCalendarRange(minDate, maxDate, dateObj){
              var maxCalendarDate = new Date(maxDate.getFullYear(), maxDate.getMonth()+1, 0);
              var minCalendarDate = new Date(minDate.getFullYear(), minDate.getMonth(), 1)
              if ( (dateObj>=minCalendarDate) && (dateObj <= maxCalendarDate)){
                return true;
              }else{
                return false;
              }
            }

              //ENABLES AND DISABLES THE MONTH AND YEAR
              scope.dateCheck= function(year, month){
                if( year ) {
                  //THIS IS THE ITERATION TO CHECK AGAINST
                  var date_to_check = new Date(year, month-1, 1);
                  return !dateInCalendarRange(scope.minDate, scope.maxDate, date_to_check );
                }else{
                  return true;
                }
              }

              scope.yearList = function(minDate, maxDate){
                var yearList = [];
                for ( var i = minDate.getFullYear(); i <= maxDate.getFullYear(); i++){
                    yearList.push(i)
                }               
                return yearList;
              }


                scope.monthList = [
                    { 'name': 'Enero', 'value' : 1 }, 
                    { 'name': 'Febrero', 'value' : 2 },
                    { 'name': 'Marzo', 'value' : 3 },
                    { 'name': 'Abril', 'value' : 4 },
                    { 'name': 'Mayo', 'value' : 5 },
                    { 'name': 'Junio', 'value' : 6 },
                    { 'name': 'Julio', 'value' : 7 },
                    { 'name': 'Agosto', 'value' : 8 },
                    { 'name': 'Septiembre', 'value' : 9 },
                    { 'name': 'Octubre', 'value' : 10 },
                    { 'name': 'Noviembre', 'value' : 11},
                    { 'name': 'Diciembre', 'value' : 12 }
                ];

                scope.dateselect = function(){
                  if(scope.years && scope.months){
                    var selectedDate = new Date(scope.years, scope.months-1, 1);
                    ngModel.$setViewValue(selectedDate);                   
                  }

                }

           }
           return directive;

    });




    //RE VALIDATES THE DATE TYPE INPUT FIELD
    mainApp.directive("datecheck", function() {
        return {
            restrict: "A",
            require: "ngModel",
             
            link: function(scope, element, attributes, ngModel) {
                ngModel.$validators.datecheck = function(modelValue) {
                  if (modelValue){
                    //alert(modelValue.toUTCString())
                    var yyyy = modelValue.getUTCFullYear().toString();
                    var mm = (modelValue.getMonth()+1).toString(); // getMonth() is zero-based
                    var dd  = modelValue.getDate().toString();
                    var dateAsString = ( yyyy +"-"+ (mm[1]?mm:"0"+mm[0]) +"-"+(dd[1]?dd:"0"+dd[0])); // padding
                    var rawVal = element.val();
                    return dateAsString == rawVal;
                  }else if(!modelValue){
                    return true;
                  }
                }
            }
        };
    });

    




    mainApp.directive("checkrif", function() {
        return {
            restrict: "A",
            require: "ngModel",
            // scope: {
            //   acceptedprefixes: '@checkrif'
            // },
             
            link: function(scope, element, attributes, ngModel) {
                ngModel.$validators.checkrif = function(modelValue) {
                  if (modelValue){
                    var allowedFirstLetter = ['J', 'j' , 'v', 'V', 'g', 'G'];
                    var rest_of_string = String(modelValue).substring(1, String(modelValue).length);
                    var rest_of_string_isnum = /^\d*$/.test(rest_of_string);
                    var string_has_spaces = (String(modelValue).indexOf(' ') !== -1);
                    var hit = allowedFirstLetter.indexOf(modelValue[0]);
                    if (hit == -1 || string_has_spaces || !rest_of_string_isnum ){
                      return false;
                    }else{
                      return true;
                    }
                  }
                  
                }
            }
        };
    });



  






//THIS DIRECTIVE TAKES AN ARRAY DICTIONARY VALUE AND IF IT CONTAINS 'notAnOption' it will make it invalidate
    mainApp.directive("validateselect", function() {
        return {
            restrict: "A",
            require: "ngModel",
             
            link: function(scope, element, attributes, ngModel) {
                ngModel.$validators.validateselect = function( modelValue ) {
                    if ('notAnOption' in modelValue){
                      return false;
                    }else{
                      return true;
                    }
                }
            }
        };
    });

    mainApp.directive('fileInputExtTarget', function () {
           var directive = {};
           directive.restrict = 'EA';
           directive.transclude = true;
           directive.scope = {
                name :'@',
                externalthumbnailId : '@',
                extChosenFileId : '@?',
                saveStatus : '=?'
                //logo_path : '&?'
                // placeholder :'@',
                // ngclass : '@',
                //ngRequired:'@ngRequired',//DONT USE REQUIRED USE NG-REQUIRED

           };
           directive.require = '?ngModel';
           directive.templateUrl = '/static/directiveTemplates/file_input.html';
           directive.link = function(scope, element, attributes, ngModel) { 
                
                var input = document.getElementById('id_fileInputDirective');
                var externalelement = angular.element(document.getElementById(scope.externalthumbnailId));
                externalelement.css('cursor', 'pointer');
                externalelement.bind('click', function () {
                    document.getElementById('id_fileInputDirective').click();
                    scope.$apply()
                });
                element.bind('change', function () {
                    var newVal = input.value;
                    extFileName = angular.element(document.getElementById('chosenFileName'))
                    extFileName.text(newVal)
                    var reader = new FileReader();
                    // if (scope.saveStatus){
                    //   scope.saveStatus = '( No ha guardado cambios )';
                    // }
                    /////TESTING/////
                    scope.saveStatus = '( No ha guardado cambios )'
                    reader.onload = function (e) {
                      ngModel.$setViewValue(e.target.result);
                        scope.$apply(function () {
                            var externalelement = document.getElementById(scope.externalthumbnailId);
                            externalelement.src = reader.result;
                            
                        });
                    }
                    
                    //alert(input.files)
                    reader.readAsDataURL(input.files[0]);
                    //alert(reader.readAsDataURL(input.files[0]))
                    //alert(document.getElementById(scope.externalthumbnailId).id)
                    //document.getElementById(scope.externalthumbnailId).src = reader.readAsDataURL(input.files[0]);
                    //scope.logo_path = reader.readAsDataURL(input.files[0]);
                    
                    var extensionName = newVal.slice((Math.max(0, newVal.lastIndexOf(".")) || Infinity) + 1);
                    var isInList = (String(attributes.extensions).indexOf(extensionName) != -1);
                    if( attributes.extensions ){
                        if ( isInList == false || !extensionName){
                            ngModel.$setValidity( 'extensions', false );
                        }else{
                            ngModel.$setValidity( 'extensions', true );
                        }
                    }

                    if (attributes.required){
                        if(ngModel){
                            ngModel.$setValidity( 'required', true );
                        }else{
                            ngModel.$setValidity( 'required', false );
                        }    
                    }
                    scope.$apply();
                });
           };
           return directive
    });


    mainApp.directive('fileInput', function () {
           var directive = {};
           directive.restrict = 'E';
           directive.transclude = true;
           directive.scope = {
                name :'@'
                // placeholder :'@',
                // ngclass : '@',
                //ngRequired:'@ngRequired',//DONT USE REQUIRED USE NG-REQUIRED

           };
           directive.require = 'ngModel';
           directive.templateUrl = '/static/directiveTemplates/file_input.html';
           directive.link = function(scope, element, attributes, ngModel) { 

                element.bind('click', function () {
                    document.getElementById('id_fileInputDirective').click();
                    scope.$apply()
                });
                element.bind('change', function () {
                    var newVal = document.getElementById('id_fileInputDirective').value;
                    var extensionName = newVal.slice((Math.max(0, newVal.lastIndexOf(".")) || Infinity) + 1);
                    var isInList = (String(attributes.extensions).indexOf(extensionName) != -1);
                    ngModel.$setViewValue(newVal);
                    if( attributes.extensions ){
                      
                        if ( isInList == false || !extensionName){
                            ngModel.$setValidity( 'extensions', false );
                        }else{
                            ngModel.$setValidity( 'extensions', true );
                        }

                    }

                    // if (attributes.required){
                    //     if(ngModel){
                    //         ngModel.$setValidity( 'required', true );
                    //     }else{
                    //         ngModel.$setValidity( 'required', false );
                    //     }    
                    // }
                    scope.$apply();
                });
           };
           return directive
    });




    // mainApp.directive('fileInput', function () {
    //        var directive = {};
    //        directive.restrict = 'E';
    //        directive.transclude = true;
    //        //directive.scope = true;
    //        directive.scope = {
    //             name :'@',
    //             style :'@',
    //             placeholder :'@',
    //             ngclass : '@'
    //             //ngRequired:'@ngRequired',//DONT USE REQUIRED USE NG-REQUIRED
    //             //extensions: '@',
    //        };
    //        directive.require = 'ngModel';
    //        directive.templateUrl = '/static/directiveTemplates/file_input.html';
    //        directive.link = function(scope, element, attributes, ngModel) {  

    //             element.bind('click', function () {
    //                 document.getElementById('id_fileInputDirective').click();
    //                 scope.$apply()
    //             });
    //             element.bind('change', function () {
    //                 var newVal = document.getElementById('id_fileInputDirective').value;
    //                 scope.adjuntos = newVal;
    //                 var extensionName = newVal.slice((Math.max(0, newVal.lastIndexOf(".")) || Infinity) + 1);
    //                 var isInList = (String(attributes.extensions).indexOf(extensionName) != -1);
    //                 if( attributes.extensions ){
    //                     if ( isInList == false){
    //                         ngModel.$setValidity( 'extensions', false );
    //                     }else{
    //                         ngModel.$setValidity( 'extensions', true );
    //                     }
    //                 }

    //                 if (attributes.required){
    //                     if(ngModel){
    //                         ngModel.$setValidity( 'required', true );
    //                     }else{
    //                         ngModel.$setValidity( 'required', false );
    //                     }    
    //                 }
    //                 scope.$apply();
    //             });
    //        };
    //        return directive
    // });


    mainApp.directive('validFile', function () {
        return {
            require: 'ngModel',
            link: function (scope, el, attrs, ngModel) {
                ngModel.$render = function () {
                    ngModel.$setViewValue(el.val());
                };

                el.bind('change', function () {
                    scope.$apply(function () {
                        ngModel.$render();
                    });
                });
            }
        };
    });


    mainApp.directive("phonenumber", function() {
        return {
            restrict: "A",
             
            require: "ngModel",
             
            link: function(scope, element, attributes, ngModel) {
                ngModel.$validators.phonenumber = function(modelValue) {
                    if (!modelValue){
                      return true;
                    }
                    return modelValue % 1 === 0 && modelValue >=0 && modelValue.length >=10 && modelValue.length <= 11;
                }
            }
        };
    });


    mainApp.directive("nrocuentavzla", function() {
        return {
            restrict: "A",
             
            require: "ngModel",
             
            link: function(scope, element, attributes, ngModel) {
                ngModel.$validators.nrocuentavzla = function(modelValue) {
                    if (!modelValue){
                      return true;
                    }
                    return modelValue % 1 === 0 && modelValue  && modelValue.length ==20;
                }
            }
        };
    });

    mainApp.directive("server", function() {
        return {
            restrict: "A",
            scope : false,
            require: "ngModel", //IF THIS IS NOT PRESENT DIRECTIVE WONT WORK
             
            link: function(scope, element, attributes, ngModel) {
                scope.$watch('serverResponse',function(newValue, oldValue){
                  if( newValue != oldValue){

                      //evaluate server response
                      if (scope.serverResponse.status=='error'){
                        scope.resetPwdForm.email.$setValidity('server', false);
                      }else if(scope.serverResponse.status =='success'){
                        scope.resetPwdForm.email.$setValidity('server', true);
                      }

                  } 
                  //scope.$apply();
                })

                scope.$watch( attributes.ngModel, function(newValue, oldValue){
                  if( newValue != oldValue){
                    scope.resetPwdForm.email.$setValidity('server', true)
                  } 
                  //scope.$apply();
                })

                // if (scope.serverResponse){
                //    scope.sersverResponse.on("change", function() {
                //       alert(scope.serverResponse)
                //       //scope.$apply(attrs.onKeyup);
                //     });      
                // }


            }
        };
    });


mainApp.directive('loading', ['$http', function ($http) {
    return {
        restrict: 'A',
        scope:true,
        link: function (scope, elm, attrs) {
            scope.isLoading = function () {
                return $http.pendingRequests.length > 0;
            };
            scope.$watch(scope.isLoading, function (v) {
                if (v) {
                    elm.css('visibility', 'visible');
                } else {
                    elm.css('visibility', 'hidden');

                }
                //scope.$apply();
            });
        }
    };
}]);

mainApp.directive('convertToNumber', function() {
  return {
    require: 'ngModel',
    link: function(scope, element, attrs, ngModel) {
      ngModel.$parsers.push(function(val) {
        return parseInt(val, 10);
      });
      ngModel.$formatters.push(function(val) {
        return '' + val;
      });
    }
  };
});

mainApp.filter('humanizetimedelta', function() {//takes a
  return function(input) {
    var delta = input;
    if (input!=null){
      var delta =  (delta)/1000;
      // calculate (and subtract) whole days
      var days = Math.floor(delta / 86400);
      delta -= days * 86400;

      // calculate (and subtract) whole hours
      var hours = Math.floor(delta / 3600) % 24;
      delta -= hours * 3600;

      // calculate (and subtract) whole minutes
      var minutes = Math.floor(delta / 60) % 60;
      delta -= minutes * 60;
      // what's left is seconds
      var seconds = delta % 60;  // in theory the modulus is not required
      result = {};
      result.days = days;
      result.hours = hours;
      result.minutes = minutes;
      result.seconds = seconds;
      // if( scope.startdate > scope.endate ){
      //     alert(expired);
      //     return false;
      // }
          if (delta < 0 ){
            return 'Concluida';
          }
          else if (days > 1){
              var difference = String(days) + ' dias ' +  String(hours) + ' horas ';
          }else if(days == 1){
              difference = String(days) + ' dia ' +  String(hours) + ' horas ';
          }else if( days < 1){
              var difference = String(hours) + ' horas ' + String(minutes) + ' minutos ' + String(seconds.toFixed(0)) + ' s';
          }else if(hours == 1){
              var difference = String(hours) + ' hora ' +  String(minutes) + ' minutos ' + String(seconds.toFixed(0)) + ' s';
          }else if( hours < 1){
              var difference = String(minutes) + ' minutos ';
          }else if( minutes == 1){
              var difference = String(minutes) + ' minuto ';
          }

      return difference;
    }

  }
});


mainApp.filter('capitalize', function() {
  return function(input, scope) {
    if (input!=null){
      input = input.toString().toLowerCase();
      return input.substring(0,1).toUpperCase()+input.substring(1);    
    }

  }
});

    // mainApp.filter('capitalize', function() {
    //     return function(input) {
    //       return (!!input) ? input.charAt(0).toUpperCase() + input.substr(1).toLowerCase() : '';
    //     }
    // })

    // mainApp.filter('venezuelanBsf', function() {
    //     return function(input) {
    //         var prefix = "Bs. ";
    //         var input = parseFloat(input);
    //         if (isNaN(input)){
    //             return '';
    //         }else{
    //             var inputString = (input.toLocaleString("es-VE"));
    //             var output = prefix + inputString;
    //             if (input < 0){
    //               output = '( '+output+' )';
    //             }
    //             return output;           
    //         }

    //     };
    // })

    mainApp.filter('firstlettereachword', function() {
        return function(input) {
            var splitStr = input.toLowerCase().split(' ');
             for (var i = 0; i < splitStr.length; i++) {
                 splitStr[i] = splitStr[i].charAt(0).toUpperCase() + splitStr[i].substring(1);     
             }
             return splitStr.join(' ');
        };
    })


    mainApp.filter('countobject', function() {
        return function(input) {
          if(input){
            return input.length;
          }else{
            return 0;
          }
        };
    })

    mainApp.filter('pagination', function()
    {
     return function(input, start)
     {
      start = +start;
      return input.slice(start);
     };
    });

    mainApp.filter('nrocuenta', function() {

        return function( input ) {

            if ( !input ) { return ''; }
            var input = String(input);
            switch ( input.length ) {
                        case 20: // +1PPP####### -> C (PPP) ####-####-####-####
                            var output1 = input.slice( 0, 4 );
                            var output2 = input.slice( 4, 8 );
                            var output3 = input.slice( 8, 10 );
                            var output4 = input.slice( 10, 20 );
                            //var output5 = input.slice( 14, -1 );
                            var output = output1 + '-' + output2 + '-' + output3 + '-'  + output4;
                            break;

                        default:
                            return input;
                    }

                return output;

        };
    })


    mainApp.filter('telephonenumber', function() {

        return function( input ) {

            if ( !input ) { return ''; }
            var input = String(input);
            switch ( input.length ) {
                        case 11: // +1PPP####### -> C (PPP) ####-####-####-####
                            var output1 = input.slice(0, 4);
                            var output2 = input.slice(4, 7);
                            var output3 = input.slice(7, 11);
                            var output = '('+ output1 + ')' + ' ' + output2 + '-' + output3; 
                            break;
                        case 10: // +1PPP####### -> C (PPP) ####-####-####-####
                            var output1 = input.slice(0, 3);
                            var output2 = input.slice(3, 6);
                            var output3 = input.slice(6, 10);
                            var output = '('+ output1 + ')' + ' ' + output2 + '-' + output3; 
                            break;                            
                        default:
                            return input;
                    }

                return output;

        };
    })

    mainApp.factory('postRequest', function( $http, $httpParamSerializerJQLike ){

        return {

            // paymentSheet: function( Obj ) {
            //     return $http({ 
            //         method: 'POST', 
            //         url: '.', 
            //         data: $httpParamSerializerJQLike(Obj),
            //         headers: {
            //             'Content-Type': 'application/x-www-form-urlencoded;'
            //         }
            //     })
            // },
            ajaxGet: function( url ) {
                return $http({ 
                    method: 'GET', 
                    url: url
                })
            },
            ajaxPost: function( url, Obj ) {
                if(!url){
                  var url = '.';
                }
                return $http({ 
                    method: 'POST', 
                    url: url, 
                    data: $httpParamSerializerJQLike(Obj),
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded;'
                    }
                })
            }
        };             
    });


Date.prototype.addDays = function(days) {
    this.setDate(this.getDate() + parseInt(days));
    return this;

};


function Screen() {
    var w = window,
        d = document,
        e = d.documentElement,
        g = d.getElementsByTagName('body')[0]

    this.height = w.innerHeight|| e.clientHeight|| g.clientHeight;
    this.width = w.innerWidth || e.clientWidth || g.clientWidth;
}


Date.prototype.toISODate= function(){
    return String(this.getFullYear() + "-" + (this.getMonth() + 1) + "-" + 1);
}

Date.prototype.toUTC= function(){
var now_utc = new Date(this.getUTCFullYear(), this.getUTCMonth(), this.getUTCDate(),  this.getUTCHours(), this.getUTCMinutes(), this.getUTCSeconds());
    return now_utc;
}




Date.prototype.monthDays= function(){
    var d= new Date(this.getUTCFullYear(), this.getMonth()+1, 0);
    return d.getDate();
}


function GetCardType(number)
{            
    var re = new RegExp("^4");
    if (number.match(re) != null)
        return "Visa";

    re = new RegExp("^(34|37)");
    if (number.match(re) != null)
        return "American Express";

    re = new RegExp("^5[1-5]");
    if (number.match(re) != null)
        return "MasterCard";

    re = new RegExp("^6011");
    if (number.match(re) != null)
        return "Discover";

    return "";
}

mainApp.directive('checkFileSize', function() {
  return {
    link: function(scope, elem, attr, ctrl) {
      function bindEvent(element, type, handler) {
        if (element.addEventListener) {
          element.addEventListener(type, handler, false);
        } else {
          element.attachEvent('on' + type, handler);
        }
      }

      bindEvent(elem[0], 'change', function() {
        alert('File size:' + this.files[0].size);
      });
    }
  }
});