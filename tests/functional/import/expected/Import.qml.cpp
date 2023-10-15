using namespace QtQuick;
using namespace QtQuick::Controls;
using namespace QtQuick::Layouts;
class Import : public QtQml.QtObject {
public:

Q_PROPERTY(string import_hello READ dummyGetter_import_hello_ignore)

Q_PROPERTY(string hello_import READ dummyGetter_hello_import_ignore)

Q_PROPERTY(string import_2_15 READ dummyGetter_import_2_15_ignore)
};
