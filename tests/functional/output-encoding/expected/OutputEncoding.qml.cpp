using namespace QtQuick;
/// @brief Output encoding test case
class OutputEncoding : public QtQuick.Item {
public:
/// @brief Text with special chars áâäà éêè íîì óôöò úûüù
Q_PROPERTY(int foo READ dummyGetter_foo_ignore)
};
