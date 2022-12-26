# python
# Listener code by Andreas Ranman

import lx
import lxifc


class RenderListener(lxifc.RenderProgressListener):
    # Render Progress Listener with callbacks on success and abort.

    def __init__(self, onSuccess=None, onAbort=None):
        # Validate that callbacks are callable
        assert (callable(onSuccess)), "onSuccess was not a callable."
        assert (callable(onAbort)), "onAbort was not a callable."

        # Callbacks for successful renders and aborts.
        self.onSuccess = onSuccess
        self.onAbort = onAbort

        # Create and add listener
        self.lisenerService = lx.service.Listener()
        self.COM_object = lx.object.Unknown(self)
        self.lisenerService.AddListener(self.COM_object)

        # Get services we want to use
        self.undoService = lx.service.Undo()
        self.renderService = lx.service.Render()

        # Variable to store the current render job in
        self.job = None

    def remove(self):
        """ Remove this listener. """
        self.lisenerService.RemoveListener(self.COM_object)

    def rndprog_Begin(self):
        """ Get the job for current render. """
        self.job = self.renderService.JobCurrent()

    def rndprog_End(self, stats):
        try:

            if not self.undoService.State() == lx.symbol.iUNDO_ACTIVE:
                # According to documentation one should safeguard against missing
                # undo states and just return.
                lx.out("No active undo state.")
                return

            # Getting the status of current renderjob will raise a runtime error
            # for when user aborted the render.
            self.renderService.JobStatus()

            self.onSuccess()

        except RuntimeError as e:
            # User likely aborted.
            self.onAbort()

        except:
            # Something actually went wrong, raise the exception and log it
            lx.out(traceback.format_exc())
            raise

        # finally:
        #     # No matter how the render finished, we want to remove the listener
        #     self.remove()
