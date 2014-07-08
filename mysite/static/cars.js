
var js_debug = true
function _log() { if (js_debug) { console.log(arguments) } }

$(function(){
  _.mixin(_.str.exports()) /* underscore + string. */

  /* note that w_* properties & variables point to jquery widgets/elements. */
  var w_dt = $('#dt')
  var w_cal = $('#cal')

  $(document).on('click', '.act', function(){
	var w_act = $(this)
	var car_id = w_act.data('car')
	var car = data.cars[car_id]
	_log('click', w_act, car_id, car)
  })

  _log('data', data)
  var data_cars = _(data.cars).values()

  _(data_cars).each(function(each){
	_(each).extend({
	  act: _('<button class="btn btn-primary btn-sm act" data-car="%s">Select</button>').sprintf(each.id)
	})
  })

  w_dt.dataTable({
    // paging: false,
    // filter: false,
    // info: false,
    columns: [
	  { title: 'Owner', data: 'owner_name' },
	  { title: 'Make', data: 'make_name' },
	  { title: 'Model', data: 'model_name' },
	  { title: 'Engine', data: 'engine_name' },
	  { title: 'Year', data: 'year' },
	  { title: 'Plate', data: 'plate' },
	  { title: 'Select', data: 'act', sortable: false },
	],
	data: data_cars
  })
  var api = w_dt.api()

  // var events = [ { allDay: true, start: '2014-07-09', end: '2014-07-10', title: 'My EVENT' } ]
  var events = _(_(data.services).values()).collect(function(each){
	return { allDay: false, start: each.start || each.sched, end: each.end, title: each.car_name }
  })

  w_cal.fullCalendar({
	header: {
		left: 'prev,next today', // prevYear,X,nextYear
		center: 'title',
		right: 'month,agendaWeek,agendaDay' // ,basicWeek,basicDay
	},
	selectable: true,
	selectHelper: true,
	select: function(start, end, allDay, ev, view) {
	  _log('cal.select')
	},
	dayClick: null, // otherwise it will trigger "select" again.
	editable: true, // draggable & resizable events.
	eventDrop: function(calev, dayDelta, minuteDelta, allDay, revertFunc, ev, ui, view) { // http://arshaw.com/fullcalendar/docs/event_ui/eventDrop/
		_log('cal.eventDrop')
	},
	eventResize: function(calev, dayDelta, minuteDelta, revertFunc, ev, ui, view) { // http://arshaw.com/fullcalendar/docs/event_ui/eventResize/
		_log('cal.eventResize')
	},
	eventClick: function(calev, ev, view) {
	  _log('cal.eventClick')
	},
	events: events
  })






  function go(city, w_button) {
	_log('go', city, w_button)
	w_button.button('loading')
	$.ajax({
	  url: 'city',
	  data: { city: city },
	  type: 'get',
	  dataType: 'json',
	  complete: function(xhr, text_status){
		_log('ajax COMPLETE', text_status, xhr)
		w_button.button('reset')
		data = xhr.responseJSON
		if (data && data.error) { return alert(data.error) } // regardless of status.
		if (xhr.status != 200) {
		  _log('ajax ERROR', xhr)
		  return alert('Error communicating to the server, please try again. If the error persists, please contact x@x.com.')
		}
		if (!data) { return alert('Ajax success, but NO data returned, please try again.') }
		_(data).extend({
		  refresh: _('<button class="btn btn-default refresh" data-city="%s">Refresh</button>').sprintf(city)
		})
		if (w_button.is(w_go)) {
		  var dt_row = api.row.add(data)
		  var w_row = $(dt_row.node())
		  w_city.val('')
		}
		else {
		  var w_row = w_button.closest('tr')
		  var dt_row = api.row(w_row)
		  dt_row.data(data) // replace.
		}
		api.draw()
		_log('go > row', w_row, dt_row)
		// w_row.addClass('selected')
	  }
	})
  }

  $('form').submit(function(event){
	event.preventDefault()
	_log('form SUBMIT')
	var city = _(w_city.val()).trim()
	if (!city) { return alert('Please enter a city.') }
	go(city, w_go)
	return false
  })

})
