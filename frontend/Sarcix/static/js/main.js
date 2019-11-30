(function () {
  // Bind events
  $('#original-modal-btn').click(openOriginalModal);
  $('#naive-modal-btn').click(fetchNaive);
  $("#analysis").click(showAnalysis);
  $('#fupload').submit(fileUpload);

  // Fetch onload data
  getRun();
})();

function showAnalysis() {
  var data = {};

  if ($('#run').length > 0) {
    data['run'] = $("#run")[0].value;
  }

  $.ajax({
    type: "GET",
    url: "/get_analysis",
    data: data,
    success: function (response) {
      $("#imagepreview").attr("src", "data:image/png;base64," + response);
      $("#imagelabel").text(data['run'] + " heatmap");
      $('#imagemodal').modal('show');
    }
  })
}

function getRun() {
  $.ajax({
    type: "GET",
    url: "/dropdowns",
    success: function (data) {
      data.forEach(function(item) {
        var item = "<option value=" + item.run_name + ">" + item.run_name + "</option>";
        $("#run").append(item);
      });
    }
  })
}

// Send file of our run to postgres
function fileUpload () {
  var file = new FormData(frm.get(0));
  $.ajax({
    type: 'POST',
    url: "/push_run_script",
    data: file,
    processData: false,
    contentType: false,
    success: function (data) {
      alert('Run was sent to your postgres db');
    },
    error: function(data) {
      alert('Form submission failed');
    }
  });
}


// Show our modal for selected run
/*Cases to be handled for title: if !empty and different (different run) -> empty content (NOT HANDLED)
if empty (first time or previously removed) -> add content  (NOT HANDLED)
else (same) -> display_modal  (HANDLED)
*/
function fetchNaive () {
  event.preventDefault();
  var send_data = {};

  if ($('#run').length > 0) {
    send_data['run'] = $("#run")[0].value;
  }
  send_data['modal_type'] = "naive"

  $.ajax({
    type: 'GET',
    url: '/run_modal',
    data: send_data,
    success: function(data) {
      openNaiveModal(data, send_data);
    },
    error: function (data) {
      alert("Failed");
    }

  });
}

function openNaiveModal(data, send_data) {
  // Check if database returned successfully return some data, check if data is empty
  if (data.hasOwnProperty('run') && data['run'][0].hasOwnProperty('run_name')) {
    var runs = data['run'].map(function (item) {
      delete item['run_name'];
      return Object.values(item);
    });
    var runName = send_data['run'];
    var currentTitle = document.querySelector(".naive-modal-title").innerHTML;
    var newTitle = "Table for run: " + runName.charAt(0).toUpperCase() + runName.slice(1).toLowerCase();

    if (currentTitle !== newTitle) {
      // If we already added this data, don't add again, just display
      // ***Makes assumption that the data that was asked for is the same as on previous attempt***

      // Add title
      $("h4.naive-modal-title").text(newTitle);

      // Add headers
      const headCols = Object.keys(data.run[0]).map(function(header){
        return "<th>" + header + "</th>";
      });
      $("thead.naive-thead tr").append([...headCols]);
    }

    $("#naive-modal").modal('show');
    var newDataTable = $('#naive-table').DataTable({
      destroy: true,
      data: runs,
      deferRender: true,
      pageLength: 100
    });
  }
}

function openOriginalModal(){
  event.preventDefault();
  var send_data = {};

  if ($('#run').length > 0) {
    send_data['run'] = $("#run")[0].value;
  }
  send_data['modal_type'] = "original"

  $.ajax({
    type: 'GET',
    url: '/run_modal',
    data: send_data,
    success: function(data) {
      // Check if database returned successfully return some data, check if data is empty
      if (data.hasOwnProperty('run') && data['run'][0].hasOwnProperty('event_name')) {
        var runs = data['run'].map(function (item) {
          return Object.values(item);
        });
        var runName = send_data['run'];
        var currentTitle = document.querySelector(".original-modal-title").innerHTML;
        var newTitle = "Table for run: " + runName.charAt(0).toUpperCase() + runName.slice(1).toLowerCase();

        // Add title
        $("h4.original-modal-title").text(newTitle);

        $("#original-modal").modal('show');

        var newDataTable = $('#original-table').DataTable({
          destroy: true,
          data: runs,
          deferRender: true,
          pageLength: 1000
        });
      }
    },
    error: function (data) {
      alert("Failed");
    }
  });
}
