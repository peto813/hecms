var hmShipModalControllers = angular.module('hmShipModalControllers',[]);



hmShipModalControllers.controller('changePwdModalController', function( $scope, $uibModalInstance, $location, $http, userSessionServices ) {

	$scope.showSuccessMessage = false;
	$scope.errors = {};
	$scope.changePwdPut = function(){
		if($scope.changePwdForm.$valid){
			data = {
				'old_password' : $scope.oldPwd,
				'new_password' : $scope.newPwd1,
				'new_password_confirm' : $scope.newPwd2
			}
			$http.put('api/changepassword/', data)
			.success(function( successResponse ){
				if(successResponse == 'Success'){
					$scope.showSuccessMessage = true;
				}
			})
			.error(function	( errorResponse ){
				$scope.errors = errorResponse;
			})
		}
	}

	$scope.cancel = function () {
		$uibModalInstance.dismiss('cancel');
	};

	// $scope.close = function(){
	// 		$uibModalInstance.close(function(){
	// 			userSessionServices.logout();
	// 		}
	// 	)
	// }
});

hmShipModalControllers.controller('regThanksModalController', function( $scope, $uibModalInstance, $location ) {

	// $scope.cancel = function () {
	// $uibModalInstance.dismiss('cancel');
	// };
	var $ctrl = this;

    $scope.close = function () {
    	$uibModalInstance.close($location.path('/home')); 
    };


});

hmShipModalControllers.controller('inspPicModalController', function( $scope, $uibModalInstance, picture ) {

	$scope.picture = picture;

	$scope.cancel = function () {
		$uibModalInstance.dismiss('cancel');
	};


});

hmShipModalControllers.controller('post_product_modalController', function( $scope, $uibModalInstance, $location ) {

	$scope.service = '';
	$scope.cancel = function () {
		$uibModalInstance.dismiss('cancel');
	};


	$scope.requestService= function(){
		$location.path($scope.service);
		$uibModalInstance.dismiss('cancel');
	}

});




hmShipModalControllers.controller('carouselLogisticsDetailModalController', function( $scope, $uibModalInstance, pdf) {


	$scope.pdf = pdf;


	$scope.cancel = function () {
		$uibModalInstance.dismiss('cancel');
	};

    // $scope.close = function () {
    // 	$uibModalInstance.close($location.path('/home')); 
    // };


});



hmShipModalControllers.controller('inspectionInfoModalController', function( $scope, $uibModalInstance, inspection_type_info, $sce ) {


	$scope.inspection_type_info = inspection_type_info;

	$scope.popover_html = '/static/templates/userapp/partials/popover/inspection_rating.html'
	$scope.cancel = function () {
		$uibModalInstance.dismiss('cancel');
	};
	//var $ctrl = this;

    // $scope.close = function () {
    // 	$uibModalInstance.close($location.path('/home')); 
    // };


});

hmShipModalControllers.controller('inspectionModalController', function( $scope, $uibModalInstance, inspection ) {


	$scope.inspection = inspection.data;
	console.log($scope.inspection)
	$scope.popover_html = '/static/templates/userapp/partials/popover/inspection_rating.html'
	$scope.cancel = function () {
		$uibModalInstance.dismiss('cancel');
	};
	//var $ctrl = this;

    // $scope.close = function () {
    // 	$uibModalInstance.close($location.path('/home')); 
    // };


});


hmShipModalControllers.controller('productPicturePreviewController', function( $scope, $uibModalInstance, mobilePhoto ) {
	
	$scope.mobilePhoto = mobilePhoto;
	$scope.cancel = function () {
		$uibModalInstance.dismiss('cancel');
	};
	//var $ctrl = this;

    // $scope.close = function () {
    // 	$uibModalInstance.close($location.path('/home')); 
    // };


});


hmShipModalControllers.controller('purchaseModifyController', function( 
$scope,
$uibModalInstance,
purchaseInfo,
auctionList,
Upload,
$uibModal,
$http
) {
	
	$scope.uploadFields =  {};
	$scope.uploadFields = purchaseInfo;
	$scope.uploadFields.auctionName = String(purchaseInfo.auction.id)
	$scope.auctionList = auctionList;

	//read file from url and put in model
	Upload.urlToBlob(purchaseInfo.image1).then(function(blob) {
		$scope.uploadFields.mobilePhoto= blob;
		$scope.selectedFile = blob
	});

	$scope.select = function(event, file) {
	    $scope.selectedFile = file;
	}

	$scope.picPreview = function(size, file){
        var modalInstance = $uibModal.open({
            ariaLabelledBy: 'modal-title',
            ariaDescribedBy: 'modal-body',
            animation: $scope.animationsEnabled,
            templateUrl: '/static/templates/userapp/partials/productPicturepreview.html',
            controller: 'productPicturePreviewController',
            size: 'md',
            resolve: {
              mobilePhoto: function(){
                return file;
              } 
            }
        });
	}

	// function getFileName() {
	// //this gets the full url
	// var url = purchaseInfo.image1;
	// //this removes the anchor at the end, if there is one
	// url = url.substring(0, (url.indexOf("#") == -1) ? url.length : url.indexOf("#"));
	// //this removes the query after the file name, if there is one
	// url = url.substring(0, (url.indexOf("?") == -1) ? url.length : url.indexOf("?"));
	// //this removes everything before the last slash in the path
	// url = url.substring(url.lastIndexOf("/") + 1, url.length);
	// //return
	// return url;
	// }

	$scope.cancel = function () {
		$uibModalInstance.dismiss('cancel');
	};
	//var $ctrl = this;

    // $scope.close = function () {
    // 	$uibModalInstance.close($location.path('/home')); 
    // };


    $scope.uploadProduct = function() {
    	var file = $scope.selectedFile
    	if ($scope.uploadProductForm.$valid){
			$scope.f = file;
		    file.upload = Upload.upload({
		      url: 'api/editproducts/' + String($scope.uploadFields.id) +'/',
		      method: 'PUT',
		      data: {
		      	auction : $scope.uploadFields.auctionName,
		      	lot_number: $scope.uploadFields.lot_number, 
		      	image1: file,
		      	description: $scope.uploadFields.description,
		      	item_name : $scope.uploadFields.item_name
		      },
		    });

		    file.upload.then(function (response) {
				$scope.uploadFields = {};
				$scope.uploadProductForm.$setUntouched();
				$scope.uploadProductForm.$setPristine();
				$scope.showSuccessMessage = true;
				$scope.selectedFile = undefined;
				alert('Product Succesfully Uploaded');
				$uibModalInstance.dismiss('cancel');
				//$scope.f = undefined;

		    }, function (response) {
		      //if (response.status > 0)
		        $scope.errorMsg = response.status + ': ' + response.data;
		    	$scope.showSuccessMessage = false;
		    }, function (evt) {
		      // Math.min is to fix IE which reports 200% sometimes
		      file.progress = Math.min(100, parseInt(100.0 * evt.loaded / evt.total));
		    });
		}
    }

});


hmShipModalControllers.controller('purchaseDetailsController', function( $scope, $uibModalInstance, item ) {
	$scope.item = item;
	$scope.services = function(obj){
		var services_list = [];
		if(obj.logistics){
			services_list.push('Logistics');
		}
		if(obj.maintenance){
			services_list.push('Maintenance');
		}
		return services_list;
	}

	$scope.cancel = function () {
		$uibModalInstance.dismiss('cancel');
	};
	//var $ctrl = this;

    // $scope.close = function () {
    // 	$uibModalInstance.close($location.path('/home')); 
    // };


});

// hmShipModalControllers.controller('searchByController', function( $scope, $uibModalInstance, $http, item1, $filter ) {
// 	//$scope.row = row;
// 	$scope.cancel = function () {
// 		$uibModalInstance.dismiss('cancel');
// 	};

// 	$scope.item1 = item1;

// 	$scope.performSearch = function(param){
// 		if($scope.searchByModalForm.$valid){
// 			// if search in current data return it
// 			if( param == 'lotNumber'){
// 				var search_param = $scope.lot_number;
// 			}
// 			if( $filter('filter')( $scope.item1, search_param ).length > 0 ){
// 				var data =  {};
// 				data.response = 'ICD';
// 				data.search_param =search_param;
// 				$uibModalInstance.close( data );
// 			}else{
// 				var base_url = 'api/auctionproducts'
// 				if($scope.searchType == 'lotNumber'){
// 					var url = base_url + '?lot_number=' + $scope.lot_number;
// 				}

// 				//var url = base_url +'api/auctionproducts?'+'lot_number=' + $scope.lot_number
// 				$http.get(url).success(function(response ){

// 					if(response.length == 0){
// 						$scope.results = '0 Results Found;'
// 					}else{
// 						var data = {searchResults:response, searchType :$scope.searchType, query_param: $scope.lot_number};
// 			    		$uibModalInstance.close( data );
// 					}
// 				})	
// 			}

// 		}
// 	}


// });

hmShipModalControllers.controller('paymentDetailsController', function( $scope, $uibModalInstance, row ) {
	$scope.row = row;
	$scope.cancel = function () {
		$uibModalInstance.dismiss('cancel');
	};

});

hmShipModalControllers.controller('orderBookDetailsController', function( $scope, $uibModalInstance, order ) {
	$scope.order = order;
	$scope.cancel = function () {
		$uibModalInstance.dismiss('cancel');
	};

});


hmShipModalControllers.controller('registerPaymentModalController', function( $scope, $uibModalInstance, bank, total, Upload, $location ) {
	
	$scope.bank = bank;
	$scope.total = total;

	function cartServiceIds(shoppingCart){
		var service_list = [];
		for (var i in shoppingCart){
			service_list.push(shoppingCart[i].id)
		}
		return service_list;
	}

	$scope.reisterBankDeposit = function(file){
    	if ($scope.registerBankDepositForm.$valid){
			
			$scope.f = file;

		    file.upload = Upload.upload({
		      url: 'api/payments/',
		      data: {
		      	//auction : $scope.uploadFields.auctionName,
		      	//lot_number: $scope.uploadFields.lotnumber,
		      	payment_type: 'deposit',
		      	//services_set : cartServiceIds(JSON.parse( sessionStorage.getItem('shoppingCart') )) ,
		      	//services_set : JSON.stringify([1, 2]),
		      	services_set :  JSON.stringify(JSON.parse(sessionStorage.getItem('shoppingCart')) ),
		      	proof: file
		      	//description: $scope.uploadFields.description,
		      	//item_name : $scope.uploadFields.item_name
		      },
		    });

		    file.upload.then(function (response, status) {
		    	if( response.status == 200 ){
		    		$uibModalInstance.close(
		    			sessionStorage.setItem('shoppingCart', '[]'),
		    			alert('Payment Succesfully Registered! We will let you know when the payment has been credited'),
		    			$location.path('paymenthistory')
		    			
		    		)
		    	}
				//$scope.uploadFields = {};
				//$scope.registerBankDepositForm.$setUntouched();
				//$scope.registerBankDepositForm.$setPristine();
				//$scope.showSuccessMessage = true;
				//$scope.selectedFile = undefined;
				//$scope.f = undefined;

		    }, function (response) {
		      if (response.status > 0)
		        $scope.errorMsg = response.status + ': ' + response.data;
		    	$scope.showSuccessMessage = false;
		    }, function (evt) {
		      // Math.min is to fix IE which reports 200% sometimes
		      file.progress = Math.min(100, parseInt(100.0 * evt.loaded / evt.total));
		    });
		    }
	}

	$scope.select = function(event, file) {
	    $scope.selectedFile = file;
	}

	$scope.cancel = function () {
		$uibModalInstance.dismiss('cancel');
	};

});


hmShipModalControllers.controller('serviceDetailsModalController', function( $scope, $uibModalInstance, service ) {
	$scope.service = service;
	console.log(JSON.stringify(service.auction_products))
	$scope.cancel = function () {
		$uibModalInstance.dismiss('cancel');
	};

});


hmShipModalControllers.controller('pendingQuoteModalController', function( $scope, $uibModalInstance, message ) {
	$scope.message = message;
	//console.log(JSON.stringify($scope.service))
	$scope.cancel = function () {
		$uibModalInstance.dismiss('cancel');
	};

});



hmShipModalControllers.controller('quoteController', function( $scope, $uibModalInstance, service, $http ) {
	//$scope.logistics = product.logistics;
	//$scope.maintenance = product.maintenance;
	$scope.hide_modal = false;
	$scope.service = service;
	$scope.cancel = function () {
		$uibModalInstance.dismiss('cancel');
	};

	$scope.respondToQuote = function(quote_approved){

		var fill;
		if (quote_approved){
			fill = 'accept'
		}else{
			fill = 'reject'
		}
		confirmation = confirm('Are you sure you wish to '+ fill + ' this quote?')
		if (!confirmation){
			return false;
		}

		$scope.hide_modal = true;

		var url = 'api/services/'+ $scope.service.id +'/';

		var params = {};
		//params.model_name = model_name;
		params.quote_approved = quote_approved;
		//if(quote_approved){

			$http.patch(url, params).success(function(service){

				//console.log(JSON.stringify(response));
				$uibModalInstance.close(service); 

			}).error(function(errors){

				console.log(errors);
			})
		//}
	}


});



hmShipModalControllers.controller('auctionDetailsModalController', function( $scope, $uibModalInstance, auctionDetails ) {
	$scope.auctionDetails = auctionDetails;
	$scope.cancel = function () {
		$uibModalInstance.dismiss('cancel');
	};
	//var $ctrl = this;

    // $scope.close = function () {
    // 	$uibModalInstance.close($location.path('/home')); 
    // };

});

hmShipModalControllers.controller('requestEmailModalController', function( $scope, $uibModalInstance, $http, $window, userSessionServices ) {
	$scope.cancel = function () {
		$uibModalInstance.dismiss('cancel');
	};

	$scope.resetValidator = function(){
		$scope.error = '';
	}

	$scope.registerEmailPost = function(){
		
		if( $scope.registerEmail.$valid ){
			var userProfile = sessionStorage.getItem('userDataString');
			var url = 'api/users/' + userProfile.id  + '/';
			var data = {};
			data.email = $scope.email;
			data.email_confirm = $scope.emailConfirm;
			//data.transaction_type = 'register_email';
			$http.patch( url, data ).success( function( response, status ){

				if( status == 200 ){
					//update the session DATA
					userSessionServices.updateSessionStorage(response);
					//console.log(response)
					//console.log(JSON.stringify(response))
					//var userInstance = JSON.parse($window.sessionStorage.getItem('userDataString'));
					//userInstance.email = $scope.email;
					//$window.sessionStorage.setItem('userDataString', JSON.stringify(userInstance));
					$uibModalInstance.close(alert('Email succesfully registered'));

				}
			})
			.error(function(errors, status){
				// console.log(errors)
				// console.log(status)
				$scope.error = errors.email[0];

			})		
		}
	}
	//var $ctrl = this;

    // $scope.close = function () {
    // 	$uibModalInstance.close($location.path('/home')); 
    // };


});

