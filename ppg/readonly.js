window.onload = function(){
	document.getElementById('billingpremise').readOnly = true;
	document.getElementById('billingfirstname').readOnly = true;
	document.getElementById('billinglastname').readOnly = true;
	document.getElementById('billingcountryiso2a').readOnly = true;
	document.getElementById('billingstreet').readOnly = true;
	document.getElementById('billingtown').readOnly = true;
	document.getElementById('billingcounty').readOnly = true;
	document.getElementById('billingpostcode').readOnly = true;
	document.getElementById('billingcountryiso2a').readOnly = true;
	document.getElementById('billingemail').readOnly = true;
	document.getElementById('billingtelephone').readOnly = true;
	document.getElementById('billingtelephonetype').readOnly = true;

	document.getElementById('customerpremise').readOnly = true;
	document.getElementById('customerstreet').readOnly = true;
	document.getElementById('customertown').readOnly = true;
	document.getElementById('customercounty').readOnly = true;
	document.getElementById('customerpostcode').readOnly = true;
	document.getElementById('customeremail').readOnly = true;
	document.getElementById('customertelephone').readOnly = true;
	document.getElementById('customertelephonetype').readOnly = true;
	document.getElementById('customercountryiso2a').readOnly = true;

	document.getElementById('block-billing-details').style.display = "none"
	document.getElementById('block-delivery-details').style.display = "none"
}