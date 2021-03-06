module Execute32 where
import Decode
import Program
import qualified CSRField as Field
import ExecuteI as I
import ExecuteM as M
import ExecuteCSR as CSR
import Control.Monad
import Control.Monad.Trans.Maybe

execute :: (RiscvProgram p t u) => Instruction -> p ()
execute InvalidInstruction = do
  raiseException 0 2
  cycles <- getCSRField Field.MCycle
  setCSRField Field.MCycle (cycles + 1)
execute inst = do
  _ <- runMaybeT (msum (map (\f -> f inst) [I.execute, M.execute, CSR.execute]))
  cycles <- getCSRField Field.MCycle
  setCSRField Field.MCycle (cycles + 1)
  instret <- getCSRField Field.MInstRet
  setCSRField Field.MInstRet (instret + 1)
