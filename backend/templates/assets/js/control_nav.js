$('.highlight').click(function() {
	$('.highlight').removeClass('active');
	$(this).addClass('active');
});

$('.btn-inst').click(function () {
	chart.expandAll();
	chart.setUpToTheRootHighlighted("").render().fit()
	setTimeout(function() {
		$('.instance').closest('div').css('border', '5px solid #8F00FF');
	}, 800);
});
$('.btn-sub').click(function () {
	chart.expandAll();
	chart.setUpToTheRootHighlighted("").render().fit()
	setTimeout(function() {
		$('.subnet').closest('div').css('border', '5px solid #8F00FF');
	}, 800);
});
$('.btn-vpc').click(function () {
	chart.expandAll();
	chart.setUpToTheRootHighlighted("").render().fit()
	setTimeout(function() {
		$('.vpc').closest('div').css('border', '5px solid #8F00FF');
	}, 800);
});
$('.btn-igw').click(function () {
	chart.expandAll();
	chart.setUpToTheRootHighlighted("").render().fit()
	setTimeout(function() {
		$('.igw').closest('div').css('border', '5px solid #8F00FF');
	}, 800);
});
$('.btn-ngw').click(function () {
	chart.expandAll();
	chart.setUpToTheRootHighlighted("").render().fit()
	setTimeout(function() {
		$('.ngw').closest('div').css('border', '5px solid #8F00FF');
	}, 800);
});
$('.btn-s3').click(function () {
	// $('.s3-box').addClass('active');
	// setTimeout(function() {
	// 	$('.s3-box').removeClass('active');
	// }, 2000);
	chart.expandAll();
	chart.setUpToTheRootHighlighted("").render().fit()
	setTimeout(function() {
		$('.s3').closest('div').css('border', '5px solid #8F00FF');
	}, 800);
});

$('.closebtn').click(function () {
	$(".sidenav").removeClass('animate');
});

function openSideNav() {
	document.getElementsByClassName('sidenav').width = '350px';
}

function openAll() {
	chart.expandAll();
	chart.setUpToTheRootHighlighted("").render().fit()
}
function closeAll() {
	chart.collapseAll();
	chart.setUpToTheRootHighlighted("").render().fit()
}