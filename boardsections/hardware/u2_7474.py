"""Simulate the 7474 IC"""

from typedefinitions import TTL

class FlipFlop:
    def __init__(self) -> None:
        self._clear_inv: TTL = TTL.H
        self._preset_inv: TTL = TTL.H
        self.data: TTL = TTL.L
        self.set_output()

    def set_output(self) -> None:
        if self._preset_inv==TTL.L and self._clear_inv==TTL.L:
            self.q_output = TTL.H
            self.q_inv_output = TTL.H
            raise Warning("Active PRE and CLR at the same time is invalid")
        self.q_output = self.data
        self.q_inv_output = ~self.data
        self.output_changed()

    @property
    def clear_inv(self): pass
    @clear_inv.setter
    def clear_inv(self, clr_inv_value: TTL) -> None:
        self._clear_inv = clr_inv_value
        # HIGH->LOW change does the clear
        if ~clr_inv_value:
            self.data = TTL.L
            self.set_output()

    @property
    def preset_inv(self): pass
    @preset_inv.setter
    def preset_inv(self, pre_inv_value: TTL) -> None:
        self._preset_inv = pre_inv_value
        # HIGH->LOW change does the preset
        if ~pre_inv_value:
            self.data = TTL.H
            self.set_output()


    def output_changed(self) -> None:
        """Called when output changes on the flip-flop output

        This happens
        - at init, to set the initial TTL levels in the CPU
        - normally on the clock LOW->HIGH edge, to set the actual TTL levels
        - at clear or preset (asyncronous from clock)
        
        Child classes must implement this method.
        """
        raise NotImplementedError
