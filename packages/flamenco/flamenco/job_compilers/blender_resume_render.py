from application.modules.flamenco.utils import frame_range_parse
from application.modules.flamenco.utils import frame_range_merge


class JobCompiler:

    def __init__(self):
        pass

    @staticmethod
    def compile(job, create_task):
        """The Blender render job with resume options."""
        job_settings = job['settings']
        parsed_frames = frame_range_parse(job_settings['frames'])
        chunk_size = job_settings['chunk_size']

        try:
            render_output = job_settings['render_output']
        except KeyError:
            render_output = render_output_from_filepath(job_settings['filepath'])

        cycles_num_chunks = job_settings['cycles_num_chunks']
        for cycles_chunk in range(1, cycles_num_chunks + 1):

            for i in range(0, len(parsed_frames), chunk_size):
                commands = []

                frames = frame_range_merge(parsed_frames[i:i + chunk_size])
                cmd_render = {
                    'name': 'blender_render',
                    'settings': {
                        'filepath': job_settings['filepath'],
                        'format': job_settings['format'],
                        'frames': frames,
                        'cycles_num_chunks' = cycles_num_chunks,
                        'cycles_chunk' = cycles_chunk,
                    }
                }
                if render_output:
                    cmd_render['settings']['render_output'] = render_output

                commands.append(cmd_render)

                # merge the files together
                if cycles_chunk == 1:
                    for frame in parsed_frames[i:i + chunk_size]:
                        input_image_render = filepath_from_frame(render_output, frame, file_format)
                        output_image_merge = merge_filepath_from_filepath(input_image_render)

                        cmd_move = {
                            'name': 'move_file',
                            'settings': {
                                'input_file': input_image_render,
                                'output_file': output_image_merge,
                                },
                            }
                        commands.append(cmd_move)

                else:
                    for frame in parsed_frames[i:i + chunk_size]:
                        input_image_render = filepath_from_frame(render_output, frame, file_format)
                        output_image_merge = merge_filepath_from_filepath(input_image_render)
                        input_image_merge = merge_filepath_from_filepath(input_image_render, "_merge_temp")

                        cmd_move = {
                            'name': 'move_file',
                            'settings': {
                                'input_file': output_image_merge,
                                'output_file': input_image_merge,
                                },
                            }
                        commands.append(cmd_move)

                        cmd_merge = {
                            'name': 'imagemagick_convert',
                            'settings': {
                                'input_image_render': input_image_render,
                                'input_image_merge': input_image_merge,
                                'output_image_merge': output_image_merge,
                                'cycles_chunk' = cycles_chunk,
                                }
                            }
                        commands.append(cmd_merge)

                        cmd_delete = {
                            'name': 'delete_file',
                            'settings': {
                                'filepath': input_image_merge,
                                },
                            }
                        commands.append(cmd_delete)

                create_task(job, commands, frames)

            # move the merged images to the correct location
            commands = []
            for frame in parsed_frames:
                input_image_render = filepath_from_frame(render_output, frame, file_format)
                output_image_merge = merge_filepath_from_filepath(input_image_render)

                cmd_move = {
                    'name': 'move_file',
                            'settings': {
                                'input_file': output_image_merge,
                                'output_file': image_image_render,
                                },
                            }
                commands.append(cmd_move)

            frames = frame_range_merge(parsed_frames[i:i + chunk_size])
            create_task(job, commands, frames)


def filepath_from_frame(render_output, frame, file_format):
    # TODO do it for real, with smart path handling or call blender and get it from it
    return "{0}/{1}.{2}".format(render_output, frame, file_format)


def render_output_from_filepath(filepath):
    # TODO use BAM, or blender output
    return "/tmp/"


def merge_filepath_from_filepath(filepath, merge="_merge"):
    """Add _merge before file suffix"""
    return "{0}{1}.{2}".format(filepath[:-4], merge, filepath[-3:])

