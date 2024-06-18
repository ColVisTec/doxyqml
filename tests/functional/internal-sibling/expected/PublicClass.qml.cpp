namespace demo {
/**
 * A class intended to appear in public documentation
 */
/** \n <br><b>Import Statement</b> \n @code import demo @endcode */
/** @version 1.0 */
class PublicClass : public QtQml.QtObject {
public:
/**
 * Some random property
 */
Q_PROPERTY(int foo READ dummyGetter_foo_ignore)
};
}
