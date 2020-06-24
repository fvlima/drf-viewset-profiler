def test_process_response_without_renderer_context(mock_line_profiler_viewset_middleware, mock_output_writer):
    response = mock_line_profiler_viewset_middleware.process_response({}, {})

    assert response == {}
    assert mock_output_writer.flush.called is False


def test_process_response_without_line_profiler(
    mock_line_profiler_viewset_middleware, mock_output_writer, mock_http_response
):
    del mock_http_response.renderer_context["request"].line_profiler
    response = mock_line_profiler_viewset_middleware.process_response({}, mock_http_response)

    assert mock_http_response == response
    assert mock_output_writer.flush.called is False


def test_process_response_writing_output(
    mock_line_profiler_viewset_middleware, mock_output_writer, mock_http_response
):
    response = mock_line_profiler_viewset_middleware.process_response({}, mock_http_response)

    assert mock_http_response == response
    assert mock_http_response.renderer_context["request"].line_profiler.print_stats.called is True
    assert mock_output_writer.flush.called is True
