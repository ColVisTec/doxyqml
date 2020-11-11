using namespace QtQuick;
using namespace QtQuick::Controls;
using namespace QtQuick::Controls::Styles;
// import in a comment
class RelativeImport : public QtQml.QtObject {
public:

Q_PROPERTY(string import_hello READ dummyGetter_import_hello_ignore)

Q_PROPERTY(string hello_import READ dummyGetter_hello_import_ignore)
};
