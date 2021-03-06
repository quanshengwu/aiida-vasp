from aiida.orm.calculation.inline import make_inline
from aiida.orm import DataFactory


@make_inline
def modify_wannier_settings_inline(original, modifications):
    '''InlineCalculation for modifying wannier settings ('.win' file).
    :key ParameterData original: base settings, can be overridden.
    :key ParameterData modifications: additional settings and overrides.
    if original comes from a VASP2WANNIER setup and num_wann is overriden,
    num_bands will automatically be set accordingly.
    No consistency checks are performed.'''
    result = DataFactory('parameter')()
    orig_dict = original.get_dict()
    mod_dict = modifications.get_dict()

    set_num_bands = not bool(orig_dict.get('num_bands'))
    set_num_bands &= bool(mod_dict.get('num_wann'))
    set_num_bands &= bool(orig_dict.get('num_wann'))
    if set_num_bands:
        orig_dict['num_bands'] = orig_dict['num_wann']

    result.set_dict(orig_dict)
    result.update_dict(mod_dict)
    return {'wannier_settings': result}
