
var js_debug = false
function _log() { if (js_debug) { console.log(arguments) } }

$(function(){
  _.mixin(_.str.exports()) /* underscore + string. */

  /* note that w_* properties & variables point to jquery widgets/elements. */
  var w_city = $('#city')
  var w_go = $('#go')
  var w_dt = $('#dt')

  w_go.removeAttr('disabled') // fix for FF ... https://github.com/twbs/bootstrap/issues/793

  $(document).on('click', '.refresh', function(){
	var w_refresh = $(this)
	var city = w_refresh.data('city')
	go(city, w_refresh)
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

  w_dt.dataTable({
    // paging: false,
    // filter: false,
    // info: false,
    columns: [
	  { title: 'City Entered', data: 'city' },
	  { title: 'City Found', data: 'city_found' },
	  { title: 'Temperature @ Celcius', data: 'temperature' },
	  { title: 'Refresh', data: 'refresh', sortable: false },
	]
  })
  var api = w_dt.api()
})
