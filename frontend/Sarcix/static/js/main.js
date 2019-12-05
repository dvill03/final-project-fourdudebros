var lazyTablePage = 1;

var lazyData = {};

(function () {
  // Bind events
  $('#original-modal-btn').click(openOriginalModal);
  $('#naive-modal-btn').click(fetchNaive);
  $('#lazy-modal-btn').click(fetchLazy);
  $("#analysis").click(showAnalysis);

  $('.lazy-data-table').scroll(function() {
    var modal_scrollTop =  $('.lazy-data-table').scrollTop();
    var modal_scrollHeight =  $('.lazy-data-table').prop('scrollHeight');
    var modal_innerHeight =  $('.lazy-data-table').innerHeight();

    // Bottom reached:
    if (modal_scrollTop + modal_innerHeight >= (modal_scrollHeight)) {
        lazyTablePage++;
        appendToLazy();
    }
  });

  // Fetch onload data
  getRuns();
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

function getRuns() {
  $.ajax({
    type: "GET",
    url: "/dropdowns",
    success: function (data) {
      var runs = data.map(function (item) {
        return  "<option value=" + item.run_name + ">" + item.run_name + "</option>";
      });
      $("#run").append(runs);

    }
  })
}

// Show our modal for selected run
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
      lengthChange: false,
      deferRender: true,
      pageLength: 100,
    });

  }
}


function openOriginalModal(){
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
          lengthChange: false,
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

function fetchLazy () {
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
      if (!lazyData['run']) {
        lazyData['run'] = data.run;

        setInterval(function () {
          lazyTablePage++;
          appendToLazy();
        }, 100);
      }
      lazyTablePage = 1;
      openLazyModal(data, send_data);
    },
    error: function (data) {
      alert("Failed");
    }

  });
}

function appendToLazy(data) {
  var runs = lazyData['run'].slice(50 * (lazyTablePage - 1), 50 * lazyTablePage);

  // Add data row
  for (var i=0; i<runs.length; i++) {
    if (runs[i].hasOwnProperty('run_name')) {
      delete runs[i].run_name;
    }
    var vals = Object.values(runs[i])
    var newRows = vals.map(function(value) {
      return "<td>" + value + "</td>";
    });

    $("tbody.lazy-tbody").append(["<tr>", ...newRows,"</tr>"]);
  }
}

function openLazyModal(data, send_data) {
  // Check if database returned successfully return some data, check if data is empty
  if (data.hasOwnProperty('run') && data['run'][0].hasOwnProperty('run_name')) {
    var runs = data['run'];
    var runName = send_data['run'];
    var currentTitle = document.querySelector(".lazy-modal-title").innerHTML;
    var newTitle = "Table for run: " + runName.charAt(0).toUpperCase() + runName.slice(1).toLowerCase();

    if (currentTitle === newTitle) {

    } else if (currentTitle !== newTitle) {
      // If we already added this data, don't add again, just display
      // ***Makes assumption that the data that was asked for is the same as on previous attempt***
      while (document.querySelector(".lazy-tbody").childNodes.length > 0) {
        var child = document.querySelector(".lazy-tbody").childNodes[0];
        document.querySelector(".lazy-tbody").removeChild(child);
      }

      // Add title
      $("h4.lazy-modal-title").text(newTitle);

      // Add headers
      var headers = Object.getOwnPropertyNames(runs[0]);
      headers.shift();

      const headCols = headers.map(function(header){
        return "<th>" + header + "</th>";
      });
      $("thead.lazy-thead tr").append([...headCols]);
    }

    $("#lazy-modal").modal('show');
    $('#lazy-table').DataTable({
      data: runs,
      deferRender: true
    });
  }
}
