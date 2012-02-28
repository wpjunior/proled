# Make directory a package.

###############################################################################
# BBB: 12/14/2004

from error import RootErrorReportingUtility
from error import ErrorReportingUtility
from error import globalErrorReportingUtility

RootErrorReportingService = RootErrorReportingUtility
ErrorReportingService = ErrorReportingUtility
globalErrorReportingService = globalErrorReportingUtility

###############################################################################
