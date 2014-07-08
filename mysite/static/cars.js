
var js_debug = true
function _log() { if (js_debug) { console.log(arguments) } }

$(function(){
  _.mixin(_.str.exports()) /* underscore + string. */

  /* note that w_* properties & variables point to jquery widgets/elements. */
  var w_city = $('#city')
  var w_go = $('#go')
  var w_dt = $('#dt')

  w_go.removeAttr('disabled') // fix for FF ... https://github.com/twbs/bootstrap/issues/793

  $(document).on('click', '.act', function(){
	var w_act = $(this)
	var car_id = w_act.data('car')
	var car = data.cars[car_id]
	_log('click', w_act, car_id, car)
  })

  $('#clear').click(function(){
	if (!confirm('Are you sure to clear all data?')) { return }
	_log('clear')
	api.clear().draw()
	w_city.val('')
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
	  { title: 'Owner', data: 'owner' },
	  { title: 'Make', data: 'make' },
	  { title: 'Model', data: 'model' },
	  { title: 'Engine', data: 'engine' },
	  { title: 'Year', data: 'year' },
	  { title: 'Plate', data: 'plate' },
	  { title: 'Select', data: 'act', sortable: false },
	],
	data: data_cars
  })
  var api = w_dt.api()
})
